# entsog/nominations-allocations: review

Checker: Sonnet 5.5 · high, 2026-10-06. Family `nominations-allocations` (lead `nominations`; members `renominations`, `allocations`).
Built with `gridflow-build --only entsog/nominations` after the seat's compact-tick fix: succeeds. Detector `detect.mjs --json`: `[]`.

## Verdict: APPROVE

No blockers, no majors, 9 nits. The content is accurate against gridflow code, bronze and silver; the chart recomputes exactly;
the losses the page leans on (BBL company, National Gas TSO Moffat entry, National Gas TSO allocation placeholders) are real and
are stated on the page. Ship. The seat's tick fix works: at 390 the y labels read `0`, `50M`, `100M`, `150M` with their left edge at 26 px and nothing clipped.

## What I verified (all passed)

- **Chart recomputed from silver** (filter, window, `last` aggregation, pivot): all three series equal the committed `series/entsog/nominations.json` value for value.
  - Moffat (IE) entry 81,288,731 to 90,763,437, min 45,664,771 (19th), max 95,147,913 (15th).
  - Bacton (BBL) exit 100,101,159, 100,104,000, 26,304,000 ... 12,000,000 (19th), 91,224,000 (20th), 77,088,000 (21st).
  - Bacton (IUK) exit 0 on 13 to 16 and 18 to 20, null on the 17th (bronze `value: null`), 91,153,956 on the 21st.
  - Alt text and every number in the key notes match. `spec_origin: vault`; no staged spec and no authored override exist.
- **Unit:** `unit` is `kWh/d` on all 294 rows of the three tables; `generic.py` has no conversion (`value` is only cast to Float64, `strict=False`).
- **Gas-day start:** `timestamp_utc` is `period_from` (`generic.py:185-187`), bronze `periodFrom` 06:00+02:00, silver 04:00 UTC on every valued row; "starting 04:00 UTC" is true for the window shown.
- **Request URL, parameter order and encoding:** byte-identical to `request_url` in bronze `.meta.json` for 2026-09-21 and to `build_params` (limit, timeZone, from, to, indicator, periodType, pointDirection; list comma-joined, `%2C`).
- **Commands:** ingest end exclusive (`day_subwindows`, one `from=to=D` call per day), transform end inclusive; same lines as the live `physical_flows` page. No `PARTITION_SOURCE_OFFSETS` for the generic ENTSOG transformer, so no widening needed.
- **Key and duplicates:** one bronze body per day per member (14 each); `id` is unique (98 of 98) in nominations and renominations; the 4-column key is unique in all three tables (98 of 98). Allocations has 59 distinct `id`: the three National Gas TSO placeholder ids recur across days (3 + 56). Nothing repeated, nothing lost to dedup.
- **Coverage defects, all reproduced from bronze:**
  - No `UK-TSO-0004` (BBL company) record in any of the 42 bodies; the register (`operator_point_directions`) shows `UK-TSO-0004` has Bacton (BBL) `ITP-00207` entry and exit, while the connector asks for `ITP-00063` (Julianadorp/Balgzand). The key note is exact.
  - National Gas TSO Moffat `ITP-00090` entry: nomination `null` on 14 of 14 days; allocation is a placeholder with remark "Virtual Point, currently Moffat is only Unidirectional exit".
  - National Gas TSO allocation rows: 42 of 42 have `isNA` 1, `value` `""` (null in silver), `periodFrom` 05:00+02:00 (03:00 UTC), `lastUpdateDateTime` 2025-02-20, and cover all three of its points (not only Moffat).
  - `is_cmp_relevant`: String in allocations (the placeholders send `""`), Boolean in the other two; `is_na` Int64 in allocations, Null elsewhere.
  - `meta.total` against `meta.count` (limit=-1): nominations 14 against 7, renominations 14 against 7, allocations 8 against 7, in every body.
- **`lastUpdateDateTime` offsets** quoted in the notes (14 h before to 34 h after; 26 to 85 h; 28 to 170 h; National Gas TSO inside the gas day) all recompute from silver (nominations -14.0 to +33.7 h; renominations +26.1 to +85.0 h; allocations +28.6 to +170.1 h; National Gas TSO nominations +11.9 to +21.5 h).
- **GNI remark** wording quoted in `what_it_is` and the notes is the bronze text; the other operators send null `itemRemarks` on nominations and renominations.
- **Renominations Moffat claim** (body, renominations note): National Gas TSO `ITP-00090` entry 0 in August, 153,846 to 159,841 in September; 154 to 160 kWh/d below GNI `ITP-00495` exit on the days both send. Correct.
- **Notebook:** written by `scripts/run_notebooks.py`, no error outputs, read-only calls, `plot_alt` numbers match the printed table (renominated = allocated at 180,146,144 / 131,501,901 / 180,105,551; nominated 45,664,771 to 95,147,913). Renominated equals allocated exactly for the 56 Interconnector and GNI rows.
- **Eight rows:** `generated_by: gridflow-sample`, 20 and 21 September at the two Bacton points, both operators; `shape: (8, 42)`; key columns first; the guide has a line for every column except the pipeline ones.
- **Rubric greps on the rendered page:** no `locally`, `held`, `our`, `since 20`, `% of`, digits plus rows/days; em dashes 0; no `→`, middle dot, `live`, `now`, `yet`, `soon`, planned, coming, real-time. The `rows` hits are the key note "returns no rows here", "one row per ..." and `shape`. Related notes are 12 words or fewer and resolve. Family anchors `#nominations`, `#renominations`, `#allocations` exist.
- **Mirrors:** `cmp` byte-equal for all three notes. No literal `---` or em dash in the `page:` block.
- **Render:** screenshots at 1440, 1024, 768 and 390 (390 in a true 390 px iframe), light only (the site has no dark theme): hero scenery, chart and key, three wrapped request URLs, commands, folded frame and guide, notebook panel and related are all fully visible. Unfolded frame measured numerically (screenshots of the unfolded state wedged): the frame scrolls inside its own 390 px wrapper (scrollWidth 7272), the document stays at 390 with no page overflow.

## Findings

1. **nit** · `page.what_it_is` / `page.family.members[0].differs`: reads as full coverage of BBL, but BBL company's own reports are absent from all three tables, and the page says so only in the Bacton (BBL) key note ("returns no rows here"). "for the BBL, IUK and Moffat interconnections" with "nine filters" lets a reader assume nine sources. Evidence: 0 `UK-TSO-0004` records in 42 of 42 bodies; 7 of 9 filters return rows. One clause such as "two of the nine, BBL company's, return no rows" in `what_it_is` or the `raw_feed.note` would state the loss where the filters are described. The key note itself is accurate, so this is a placement nit.
2. **nit** · `page.raw_feed.note` / vault note "Known issues": `meta.total` is twice `meta.count` for nominations and renominations (14 against 7) and 8 against 7 for allocations; the page is silent and the vault says "unverified". The page makes no completeness claim, so nothing overclaims. For context, the same doubling shows on other indicators with different content in the bronze I hold (`aggregated_physical_flows` 6 against 3, `methane_content` 6 against 3, `hydrogen_content` 4 against 2) and not on `firm_*` (9 against 9), which points at a vendor-side count rather than lost rows, but that cannot be proven without a live call. Keep it in the defect log.
3. **nit** · `page.notebook.lead`: the printed `timestamp_utc` column in the notebook output reads `2026-09-13 05:00:00+01:00` (pandas in UK time), while the page says the gas day starts 04:00 UTC. Same instant, but a reader meets 05:00 under a "04:00 UTC" chart. One clause in the lead ("printed in UK time") fixes it. Evidence: `notebooks/entsog/nominations.json` cell 4 output index and rows.
4. **nit** · `page.raw_feed.commands` against `page.notebook.needs`: the commands ingest and transform only `nominations`, but the notebook queries all three members and `needs` says "all three members". Following the two lines gives empty renomination and allocation frames. The approved `ndf` family has the same shape, so this is precedent, not a regression.
5. **nit** · `page.family.members[2].differs` / guide for `timestamp_utc`: the guide (the lead's frame) says `timestamp_utc` is the gas-day start. In `allocations`, National Gas TSO's three placeholder rows carry 03:00 UTC, so the table has two `timestamp_utc` values per day, and `is_cmp_relevant` is text there. `differs` says "sends only not-applicable rows", which is true, but the stamp and dtype consequences live only in the vault Known issues. Optional: the line is at 13 of 14 words, so a fix means rewording (for example "Allocated quantity with a flow status; National Gas TSO rows are placeholders at 03:00 UTC"), or leaving it in the vault note.
6. **nit** · `page.facts.grain` / `page.record.key`: the page states the 4-column key plainly; code deduplicates on the vendor `id` (`generic.py:193-199`, which also carries `dataSet`, period type and unit), and the 4-tuple is unique only in these rows (the vault note scopes it to "2026-08/09 silver"). The `id` guide line ("one row per id") is the code-true statement. All `dataSet` values are 1 and all units `kWh/d`, so the two keys coincide here. Acceptable as the practitioner's key; flagging that it is observed, not enforced.
7. **nit** · vault bodies (`30-vendors/entsog/datasets/*.md`), silver schema tables and wording, smallest-span rule:
   - `id_point_type` is `str` in nominations and renominations but silver holds Int64 (and the author wrote Int64 in allocations); `is_na` is `str` in all three (silver: Null in nominations and renominations, Int64 in allocations); `is_cmp_relevant` is `bool` in the allocations table while the same note's Known issues says it is text there.
   - Allocations Known issues: "an `id` with no date" is followed by an id that does carry dates (`2026-01-012027-01-01_NA2`, a fixed 2026-2027 range, not the gas day). Say "no gas-day date".
   - The body link `20-domain/markets/gas-nominations.md` does not exist in the vault worktree (pre-existing, not the author's).
8. **nit** · `page.chart_view.alt`: "falls from 100,104,000 on the 14th to 12,000,000 on the 19th, then reads 77,088,000 on the 21st" skips the rise to 91,224,000 on the 20th, which the chart shows clearly. Add "rises to 91,224,000 on the 20th".
9. **nit** · `page.chart_view.key[0].note`, vault Moffat Known issue, `page.family.members[1].differs`: "virtual reverse point" and "the revision of the nomination" are domain readings. The only vendor text is the remark "Virtual Point, currently Moffat is only Unidirectional exit" (the renomination values match GNI's exit within 0.2 MWh/d, which supports "reverse" but is a project observation), and the author report says the definitions of nomination and renomination were deliberately avoided. Both are standard usage; no evidence cited. Soften to the remark's own words or cite the network code if wanted.

## Not verified

- What `meta.total` counts (needs a live call; barred here).
- Whether a later fetch changes a stored nomination (no second fetch exists).
- The unfolded frame was inspected by DOM measurement, not by screenshot.
- Dark theme: the site has none (confirmed, as the seat noted).
