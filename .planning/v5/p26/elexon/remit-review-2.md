# remit: re-review (Revision 1)

Checker, 2026-09-29. Re-checked the writer's Revision 1 against `remit-review.md`. Inputs:

- the canonical note and its mirror (`cmp` identical; CRLF 360, bare LF 0);
- a fresh `gridflow-build --only elexon/remit` (passes);
- the detector: only the accepted `em-dash-overuse` advisory; 0 `—`, 0 `→` on the page;
- silver with Polars, and bronze JSON read only for the `fuelType` claim;
- new screenshots at 1440, 1280, 1024, 768 and true 390 (390 px iframe, port 9745, server stopped), folded, and
  unfolded with the notebook open.

## Verdict: APPROVE

All seven earlier findings are fixed. The revision broke nothing. One optional nit on wording.

## Findings

1. **nit (optional)**, vault body, Known issues > Revisions bullet: "47 messages carry two numbers in the same publish
   second". 47 is right, but 8 of those messages carry three or more numbers in one second. "Two or more numbers" is
   exact. Evidence: `group_by(mrid, timestamp_utc).agg(revision_number.n_unique())`, filtered `> 1`, gives 47
   `mrid`s; `>= 3` gives 8 seconds in 8 messages.

## The earlier findings

| # | Earlier finding | Status | Evidence |
|---|---|---|---|
| 1 (major) | "32 steps" in the Revisions bullet | fixed | Now "in 4 messages a lower number was published after a higher one (3 of them one second later), and 47 messages carry two numbers in the same publish second". Matches my pairwise join: 5 row pairs across 4 messages, 3 of them 1 s apart, `...ELXP-RMT-20000025` 6 h 30 m. Also matches 72 same-second pairs across 47 messages. The re-send counts (62/42/3/6) are unchanged and still reproduce. |
| 2 | Body `event_status` "Active / Withdrawn etc." | fixed | Now `Active`, `Inactive`, `Dismissed`, "no `Withdrawn`". Silver: 1,943 / 146 / 202, no other value. |
| 3 | `key[no_fuel].note` "sends `fuelType` as null" | fixed, claim verified | See "Fuel type absent" below. |
| 4 | Key not unique (6 exact repeats) | fixed | `facts.grain` adds "sometimes identically"; the build's budget check passes. |
| 5 | `fields.timestamp_utc` "not an event time" | fixed | Now "not the outage's start or end". No longer clashes with the lineage `event_time`, which equals this column. |
| 6 | `related` uou2t14d / fou2t14d said what, not how | fixed | "Forward availability for the units these messages name" and "Forward availability for the fuel types charted here", both 12 words or fewer and relational. |

## The three things asked for

### Recounted revision sentence

The sentence reproduces, as the table above shows: 4 messages with 5 row pairs, and 47 messages with two or more
numbers in one second. The only gap is the "two" in "two numbers" (nit 1).

### Fuel type absent, not null (310 absent, 0 null)

The claim is confirmed from bronze, read only:

- September: 10 bodies, 1,401 records. `fuelType` is present with a value 1,091 times and absent 310 times. It is
  never an explicit `null` or `""`.
- August: 6 bodies, 890 records, 145 absent, 0 null.
- The absences match silver's `fuel_type` null counts exactly (Sep 310, Aug 145). So every silver null comes from a
  missing key, which `pl.DataFrame(rows)` fills (`remit.py:62-76`).
- By message type in September, absences are 262 `UnavailabilitiesOfElectricityFacilities` and 48
  `OtherMarketInformation`. Every `OtherMarketInformation` record lacks the key.
- The key's code `null` still names the silver value the chart groups on (`group_null: no_fuel`), so the code and
  the note ("Elexon's record has no `fuelType` field") agree.

### Wind key, "Wind *, 2 values"

- The note "`Wind Offshore` and `Wind Onshore` counted together." names both mapped values; they match `group_map`
  (both go to `wind`).
- It follows the hydro pattern and is not filler: the code no longer lists the values, so the note carries them.
- Wind stays 70, and its paint is unchanged.
- In the screenshots the wind and hydro entries fit their key column at every width. At 1280, "Hydro *, 2 values" is
  the widest code and still ends inside the column.

## Other checks (no finding)

- No artefact changed. The series, sample and notebook digests are unchanged and the build's digest check passes.
- Everything I approved in the first review still holds (URL, commands, frame, guide, notebook, chart counts).
- The latest-view ordering note from the first review remains a seat follow-up for gridflow, not a page defect.
- Screenshots: nothing clipped or overlapping in the hero facts (the longer grain line wraps cleanly), chart, key,
  raw feed, frame, guide, notebook or related list, at any of the five widths.
