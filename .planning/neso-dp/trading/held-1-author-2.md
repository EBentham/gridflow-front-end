# Held Trading pages, part 1: writer report, round 2 (2026-10-23)

These are fixes for `held-1-review.md`. Balancing and index-linked were APPROVE, with 3 and 4 nits. Super SEL was
REVISE, with 1 major and 3 nits. The page title is the seat's, so `page.title` is unchanged.

## Super SEL contract enactments

1. **Major, `page.held`.** It now reads: "All years are withheld together: from 2021-22, `Cost` is labelled £/h but
   described as a total." That is 16 words, and it avoids the word "held".
   - It says the 2020-21 rows go with the rest of the table.
   - It names the clash: the label is a rate, NESO's description a total.
   - Evidence: the registry has one eligibility for the whole record, and the 2020-21 bronze header has no `Cost`.
2. **Nit, `related[2]`.** The ODFM link is replaced by `neso_data_portal/constraint-breakdown`, "NESO's daily
   constraint costs, to read beside these enactments by date". The note's body points to the constraint-cost pages,
   joined by time. I did not use the checker's "minimum-generation context": the constraint breakdown's four reasons
   are largest loss, inertia, voltage and thermal, so that wording would overclaim.
3. **Nit, `facts.history`.** It now reads "NESO dates the first table from July 2020; yearly tables 2020-21 to
   2025-26" (13 words). The source is the 2020-21 resource description, "Data from July 2020".
4. **Nit, `what_it_is`.** I left it as is, as the checker allows. It is at its 60-word budget, and `how_used[1]` states
   that £/MW/hr is not £/MWh.

## Balancing services contract enactment

1. **Nit, `family.members[0].held`.** It now reads "`Cost` is labelled £/h, but NESO describes it as a total: volume
   times price times duration." That is 16 words, and the same wording is used on index-linked.
2. **Nit, the ZIP as its own key.**
   - `raw_feed.note` now reads: "From NESO's CKAN portal: one `package_show`, then each table's dump, kept if its body
     changed. The archive ZIP, listed under the older table, is its own key, `bs_contract_enactment_files`." That is
     28 words.
   - The third command's comment is now "the ZIP's own key, bronze only".
   - The ZIP request stays under the older table, as the checker recommended.
3. **Nit, "Pre June 2021".** The older member's `differs` now reads "Older table; its name, Pre June 2021, is not an end
   date" (12 words). The clause that the ZIP's files share its columns is dropped to fit, because the raw-feed note now
   carries the ZIP.

## Index-linked contract enactments

1. **Nit, `held`.** It uses the same clash wording as balancing (16 words).
2. **Nit, NESO's title.**
   - `facts.vendor` now reads "NESO Data Portal, package Index Linked Contracted Energy Volume: four datastore tables,
     one ZIP" (14 words).
   - `page.title` is unchanged: it is the seat's manifest item.
3. **Nit, the Nord Pool link.** It now reads "One GB day-ahead auction; NESO does not say which exchange it means" (12
   words). The page no longer implies that NESO's "power exchange auction" is Nord Pool's. The Nord Pool page's own
   summary is "Nord Pool's GB day-ahead auction price".
4. **Nit, the ZIP's Excel members.** I left it as is, as the checker allows. The defect is in the note and in the
   round-1 defect list.

## Gates

- The three notes are still CRLF (CR count equals line count: 516, 517, 284). Each is mirrored, and `cmp` is clean on
  all three.
- `parse_page_fields` and `anatomy_errors`: `[]` on all three. Every held line is 16 words.
- `gridflow-build --only` for `bs_contract_enactment_balancing`, `index_linked_contract_volume` and
  `ssel_contract_enactment`: all three wrote, with no errors on these pages.
  - One run printed "1 error(s) on pages not rendered by --only". That count covers only errors that do not name the
    page being built (`build.py` `_scoped`).
  - A full `gridflow-build --check` afterwards exited 0, and a fresh `--only` run printed no such line. It was another
    writer's note in mid-edit.
- **Side effect:** `--check` also re-rendered every vendor's generated HTML from the notes as they stood. Those files
  are gitignored, and no tracked file changed. Writers on other pages should rebuild their own page with `--only`
  before taking screenshots.
- The detector returns `[]` on all three.
- Rendered text has 0 em or en dashes and none of the banned words (including "held"). The viewport meta and `<main>`
  are present.
- No screenshots this round: I was told not to start a server. The changes are short prose swaps, and the longest new
  string (the raw-feed note naming `bs_contract_enactment_files`) wraps like the request URLs did in round 1.

## Defects

None new. The round-1 NESO defects stand, and the checker confirmed them. No gridflow defect.

## Follow-up (heading)

`page.title` on the index-linked note is now NESO's package title, "Index Linked Contracted Energy Volume" (5 words). The note is still CRLF (517 of 517), mirrored with `cmp` clean; `--only neso_data_portal/index_linked_contract_volume` wrote with no errors; the detector returns `[]`; the rendered h1 reads "Index Linked Contracted Energy Volume".
