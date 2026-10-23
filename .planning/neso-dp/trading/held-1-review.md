# Held Trading pages, part 1: checker review (2026-10-23)

Checked against the batch file, standing instructions, the writer's report, the three canonical note diffs against `origin/master` (vault worktree `C:\gridflow-wt\vault-neso-trd`), the mirrors, the built pages, the ledger rows (73, 75, 77), the registry hold questions, gridflow `client.py` (`iter_members`, `_dump_member`, `_frozen_not_due`), the catalogue snapshot `20261006T195819Z`, the saved field info for all four tables, `K-TRD-FACTS.md` section 3.8, bronze sidecars, bronze bodies and both ZIPs (read only, Python csv and zipfile).

Gates, all rerun by me: `gridflow-build --only neso_data_portal/<lead>` wrote all three, no errors; `cmp` canonical note against mirror clean on all three; detector `[]` on all three; no series, sample or notebook artefact exists for any of the keys; rendered `<main>` text has no em or en dashes, arrows or middle dots and none of live, now, real-time, yet, soon, pending, planned, shipped, coming, locally, ruling, ledger, TODO, held, TRD (the only hit for "rows" is the "Rows not shown" label); viewport meta present. Screenshots at 1440, 768 and 390 (390 through a 390 px iframe) on my own port 9865, in `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\trd1-checker\`; I read 1440 for the family page and Super SEL and 390 for the family page: nothing clipped or overlapping, long request URLs wrap. Server stopped by its own PID (found on the port, command line matched); 9670 untouched. Dark mode not checked.

## Reproduced

| Claim | Result |
|---|---|
| Bronze holds only the 2026-10-08 captures for all six families | Reproduced (file listing); no recapture. |
| Every request line equals the sidecar `request_url` (dumps and both ZIP download URLs); `package_show` is the connector's form | Reproduced. |
| Modern balancing: 13-column header in all five bodies; `Cost`, `SO_Flag`, `Reason` present | Reproduced. |
| Older balancing table: 79 of 79 `Start Time` cells are `YYYY-MM-DD`; all 79 `End Time` and `Last Updated` carry a time of day and none a zone suffix; dictionary unit for both is "N/A"; datastore type of `Start Time` is `date` | Reproduced (bronze; saved field info). |
| Balancing ZIP: two members, both headed with the older table's nine columns | Reproduced. |
| Index-linked ZIP: 134 members; 132 are CSV text headed `Date,SP,...` (five header variants), 2 are Excel workbooks named `.csv`; three files spell "Histroic" | Reproduced. |
| Super SEL: 2020-21 body headed `Record,Unit,Start,End,Reduction (MW),Price (£/MW/hr)`; the five later bodies carry the 13 columns including `Cost`; 2021-22 is the first | Reproduced. |
| `Cost` in all three saved dictionaries: unit £/h, description "Total cost to Nationalgrid ESO ...", comment "Cost = Volume * Price * Duration" | Reproduced, identical in all three. |
| Dumps are kept only if the body changed; frozen dumps re-checked at most weekly; uploads skipped when the capture carries the live `last_modified`; the frozen rule does not apply to the ZIP | Matches `_dump_member`, `_frozen_not_due` and the upload branch of `iter_members`. Registry: index-linked is `frozen`, the other two `daily`. |
| Resource lists: five yearly plus the older table (balancing, none for 2024-25); four yearly (index-linked); six (Super SEL) | Reproduced (snapshot and registry). |
| `dataset_version` `1+e1` is record version plus engine version (writer's correction) | `generic.py:501` and `:107` as the writer says (found in the writer's report; the note's span is correct and minimal). |
| Super SEL 2020-21 times are UTC | Rests on NESO's 2020-21 dictionary as quoted in `K-TRD-FACTS.md` section 3.8 (T02, T03). The saved field info covers only the newest resource, so I could not re-read the dictionary itself (no live call). Fine as stated. |

## Focus 1: the "Rows not shown" lines

- **Older balancing table** ("Start times are dates only, and NESO gives no clock for the end and update times"): accurate against the registry question and bronze. Plain, no codes, no local data. Good.
- **`Cost` lines** (balancing yearly tables, index-linked, Super SEL): accurate against the saved dictionaries, but they do not say what the conflict is (finding 1). Super SEL has a separate gap, the 2020-21 table (finding 2).

## Verdicts

| Page | Verdict | blocker | major | nit |
|---|---|---|---|---|
| `balancing-services-contract-enactment` | APPROVE | 0 | 0 | 3 |
| `index-linked-contract-volume` | APPROVE | 0 | 0 | 4 |
| `super-stable-export-limit-contract-enactment` | REVISE | 0 | 1 | 3 |

## 1. `balancing-services-contract-enactment` (leads `bs_contract_enactment_balancing`, `bs_contract_enactment_balancing_service`) - APPROVE

1. **nit** `page.family.members[0].held`: "NESO labels `Cost` £/h but defines it as volume times price times duration." is true, but it states the two facts and leaves the reader to work out the clash. NESO's description field calls `Cost` a "Total cost", and volume (MW) times price (£/MWh) times a duration is a sum in £, not a rate in £/h; neither the word "total" nor the unresolved question appears. Suggest, within 16 words: "`Cost` is labelled £/h, but NESO's formula, volume times price times duration, gives a total in £." (17 words; trim "in £" if needed). The same nit applies to finding 1 on the other two pages; apply one wording to all three.
2. **nit** `page.family.members[1].request` and `.differs`, `page.raw_feed.note`: the archive ZIP sits under the older table's request list, and the member's `differs` says the ZIP's two files share its columns. That is accurate (both files carry the nine older columns; the ZIP is also why the older table's clocks are in question) and I would keep the placement under the older table rather than the yearly one. It is not misleading, but a reader can take the ZIP address for part of that member's own ingest. It is fetched by its own key (`bs_contract_enactment_files`), shown only in the third command's comment ("the archive ZIP, bronze only"). Suggest `differs`: "Older table named Pre June 2021; its separate ZIP's two files share its columns", or end `raw_feed.note` with "The ZIP has its own key." Neither is required.
3. **nit** `page.family.members[1].differs`: "Older table named Pre June 2021" reads as if its rows end in June 2021. NESO's own label is wrong (the table's start dates run to 2023, in the writer's defect list). The page cannot give those dates (rows not shown), but "named" already signals a label; leave as is unless the seat wants "(the name is not a boundary)", which is 6 words and fits.

Checked and fine: `facts` (six datastore tables, one ZIP; years 2021-22 to 2026-27 with no 2024-25, as read from the 6 October snapshot; "NESO says its current file refreshes every ten minutes", NESO's "Live data file is refreshed every ten minutes"); `what_it_is` against NESO's notes (trading timescales, most cost-effective action, Scotland and reactive power examples, "no physical exchange of power or energy"); the yearly tables adding `Cost`, a flag and a reason; `differs` for the yearly member (five tables, first and newest shown, UTC); the three commands (valid keys; the transform is valid for the datastore families; the ZIP family is `kind: files`); related links (the GTMA and constraint breakdown links are supported by NESO's "trading and balancing services" and "constraint management" wording; the GTMA page renders only after the second Trading part's page lands in the same PR, a seat item); the 16-word cap (13 and 16 words).

## 2. `index-linked-contract-volume` (lead `index_linked_contract_volume`) - APPROVE

1. **nit** `page.held`: same wording gap as finding 1 on the balancing page (the clash is not stated). Use the same replacement.
2. **nit** `page.title`, `page.facts.vendor`: the page is titled "Index-linked contract enactments" but NESO's package title is "Index Linked Contracted Energy Volume" (the slug and the archive file names carry it). A reader looking for the package on NESO's site will not find the page title there. Put the NESO title in `facts.vendor`, as the voltage costs page does ("package Voltage System Costs (`outturn-voltage-costs`)"), for example "NESO Data Portal, package Index Linked Contracted Energy Volume (`index-linked-contract-volume`): four datastore tables, one ZIP". Check the word budget.
3. **nit** `page.related[2].note` ("Day-ahead exchange prices; NESO enacts these contracts before the auction"): NESO's words are "ahead of the power exchange auction", with no name. The Nord Pool page covers Nord Pool's GB day-ahead auction; NESO does not say it is that one (the writer lists this as unverified). Suggest attributing it: "Day-ahead exchange prices; NESO says it enacts these contracts before the exchange auction". The link itself is reasonable.
4. **nit** `page.what_it_is`: "An archive ZIP holds older files of volumes by date and settlement period" is right for 132 of 134 members (two are Excel workbooks named `.csv`), and it says nothing the reader can check. Leave, or add "(some Excel files named .csv)" if the seat wants the defect on the page; the note carries it.

Checked and fine: `facts` (four tables, one ZIP, "NESO gives no update frequency" since the extras carry only a status, weekly re-check matches the frozen rule); `what_it_is` (strike price, spread deducted or compensated, outturn market indices, morning enactment) against NESO's notes; the three requests plus package_show equal the sidecars; `raw_feed.note` ("first and newest shown", weekly re-check, ZIP unless `last_modified` unchanged) matches the code; commands valid (the `_files` key exists); related links to the voltage requirement, voltage costs and balancing pages resolve and their notes match those pages' own summaries; no "latest" claim.

## 3. `super-stable-export-limit-contract-enactment` (lead `ssel_contract_enactment`) - REVISE

1. **major** `page.held`: "From 2021-22, NESO labels `Cost` £/h but defines it as volume times price times duration." scopes the cost question to 2021-22 onward and says nothing about 2020-21. But the whole table is withheld, 2020-21 included (the registry has one hold for the whole record; the 2020-21 body has no `Cost` column). A reader who has just read in `what_it_is` that 2020-21 has a MW reduction and a £/MW/hr price will expect those 20 rows to be shown, and the page gives no reason why not. The line is true but its framing implies the earlier rows are free. It needs to say all years go together, within 16 words, for example: "All years stay out together: from 2021-22, `Cost` is labelled £/h but described as a total." (15 words). Avoid the word "held" (the page copy rules). This also applies the clash fix from finding 1 on the balancing page.
2. **nit** `page.related[2]` (ODFM): drop it, or swap it. The link rests only on NESO's "Downward Regulation" tag. Neither note says Super SEL is a downward flexibility service: NESO describes it as lowering the minimum generating level, not as flexibility, and the ODFM page says ODFM ran in the summers of 2020 and 2021 to reach downward flexibility outside the Balancing Mechanism. "Another NESO downward flexibility service, summers 2020 and 2021" therefore asserts a relation from a tag, and its date tail can be read as dating Super SEL (the page's own history runs to 2025-26). Better: replace it with the constraint breakdown page, which the Super SEL note's own body points to ("joined by time to the balancing and constraint-cost pages"), for example "NESO's daily constraint costs, the minimum-generation context". Dropping it leaves two links, which is allowed; replacing it keeps three.
3. **nit** `page.facts.history`: "From July 2020, NESO says" is correct (the 2020-21 resource says "Data from July 2020") but does not say it is about that resource. Suggest "NESO dates the first table from July 2020; yearly tables 2020-21 to 2025-26". Check the budget.
4. **nit** `page.what_it_is`: "later tables use NESO's enactment columns" is fine, but the page never says the two layouts hold different quantities (a capacity rate against a price), which `how_used[1]` does say. Fine as is; noted only because the how-used line is the only place the difference is stated.

Super SEL note correction (`1+e1`): correct and minimal. `generic.py:501` composes `f"{record.version}+e{ENGINE_VERSION}"` and line 107 sets `ENGINE_VERSION = "1"`; the old "record version 1, epoch 1" reading was wrong, the TODO is gone, and the surrounding sentences still agree. Nothing else in the note's body changed.

Checked and fine: `summary` and `what_it_is` against NESO's notes (lowers the minimum level, no change in output needed, trading instruction, Balancing Mechanism dispatch if required); cadence ("every ten minutes, no updates if no changes" paraphrased correctly); six tables 2020-21 to 2025-26; the 2020-21 columns and units; the three shown requests equal the sidecars; `raw_feed.note` ("2021-22, the first in the later layout") is true; commands valid; the Super SEL hold sits on the whole record, as the registry has it.

## Answers to the seat's questions

1. `Cost` wording: accurate to the saved dictionaries on all three; add the clash (nit on two pages). On Super SEL it needs the all-years framing (major).
2. ZIP under the older table: accurate and not misleading in substance; keep it there. A one-clause pointer that it has its own key would remove the one way to misread it (nit).
3. ODFM link: should go, or be swapped for the constraint breakdown page (nit).
4. `1+e1` correction: right.
5. Facts and what-it-is: true against NESO's text, the saved dictionaries, the registry and gridflow code. No blocker or fact error found.

## Defects to carry (writer's, confirmed)

- NESO's older balancing table still shows date-only start times and a label ("Pre June 2021") that its start dates outrun.
- NESO's portal still lists no 2024-25 balancing table (snapshot 6 October); the two Excel workbooks in the index-linked ZIP are still named `.csv`.
- The three `Cost` dictionaries still label £/h against a "Total cost" description.
- No gridflow defect found; the writer's Super SEL note fix is documentation only.
