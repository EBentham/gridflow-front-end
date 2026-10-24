# Held Interconnector pages, part 2: writer report (2026-10-24)

Packages: `nemolink` (`nemolink_ntc` lead, `nemolink_intraday`, `nemolink_nemo_da_id_weekly_ntcs`), `nsl` (`nsl`,
one-table page), `viking` (`viking_ntc` lead, `viking_link_ntc`). Every table held. Vault worktree
`C:\gridflow-wt\vault-neso-ic`, front-end worktree `C:\gridflow-wt\fe-neso-ic`. Nothing staged or committed. Scratch
and scripts: `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\ic-h2-writer\`.

## Gates

| Gate | Result |
|---|---|
| `cmp` canonical note against mirror | clean on all three |
| CRLF kept | CR count equals LF count in all three notes (512, 373, 385); diff shows only my spans |
| `gridflow-build --only neso_data_portal/<lead>` (`nemolink_ntc`, `nsl`, `viking_ntc`) | each wrote its page (dataset template), no errors |
| `gridflow-build --check` (full) | exit 0, "idempotent across 172 pages + 7 hubs" |
| Detector `detect.mjs --json` | `[]` on `nemolink.html`, `nsl.html`, `viking.html` |
| Artefacts | none written (held); no staged spec or authored override existed for any key |
| Rendered `<main>` text | no em or en dashes, arrows or middle dots; none of live, real-time, soon, pending, planned, shipped, locally, ruling, ledger, TODO, held, yet, E-SEM, "since 20", "our", capture; viewport meta present; every related href resolves to a built page |
| Hold lines | 15 (NemoLink current+archive), 16 (intraday), 15 (weekly), 16 (NSL), 15 and 16 (Viking); budget 16 |
| Screenshots | 1440, 1024, 768 and 390 (390 px iframe) for all three pages, port 9822, in `scratchpad\ic-h2-writer\shots\`. I looked at NemoLink 1440 and 390 and NSL 768: nothing clipped or overlapping; long URLs, keys and `nemolink_nemo_da_id_weekly_ntcs` wrap. Light mode only. Server started in Bash with its PID recorded (41572), stopped by that PID; 9670 untouched. |

## Shared wording (kept equal to part 1)

Title "<Link> transfer limits"; summary "NESO's limits on flow (each way) over <Link>, an interconnector between GB and
<country>, in MW for each hour it restricts" (NSL drops "each way" for budget); the `what_it_is` opener from NESO's
package notes; the three `how_used` lines; the raw-feed note for dump plus archive; `pipeline` per member on family
pages, `ingest` then `transform` on the one-table page; `landscape: power`.

NTC as NESO writes it: all three package titles and the current and daily-archive resource descriptions say "Net
Transfer Capacity"; NemoLink's two older resources (weekly archive, intraday file) say "NGESO's Network Transfer
Capacity". Each page says "NESO calls them Net Transfer Capacity (NTC) restrictions"; NemoLink adds "its two older
files say Network Transfer Capacity".

Hold lines, by question:
- Current table alone (Viking): the seat's shared dump line, "Nearly every hour is already past, and NESO does not say
  rows are unchanged since upload."
- Archive alone, same eligibility question as IFA's archive (rollover and GMT/BST undocumented, every target before
  `last_modified`): the shared archive line, NemoLink weekly and Viking archive.
- One table holding a dump and an archive: NemoLink `nemolink_ntc` uses ElecLink's line word for word ("NESO does not
  say current rows are unchanged since upload, or define archive days and versions."). NSL: "NESO does not say current
  rows are unchanged since upload, and the archive repeats a row." The NSL archive never loads (repeated whole row,
  adjudicated failed capture), so the repeat, not its calendar, is why it shows no rows.
- NemoLink intraday (its own question): "Rows give hours but no date; NESO explains neither the table's name nor
  whether it changes."

## Evidence (all packages)

| Claim | Evidence |
|---|---|
| NESO notes text (values submitted to capacity calculations, max GB import and export, MW per hourly period, final capacity may be lower and is on the trading facilitator's website, no values means no restriction) | catalogue snapshot `20261006T195819Z`, `notes` of all three packages (identical) |
| Cadence "Daily" (NemoLink, NSL), "Ad hoc" (Viking) | snapshot `extras` |
| "Net Transfer Capacity" vs "Network Transfer Capacity" | snapshot titles and resource descriptions (above) |
| Requests | equal to each sidecar `request_url` (both captures for dumps); `package_show` is the connector form |
| Dump kept only if body changed; upload skipped when `last_modified` unchanged | gridflow `client.py` `iter_members` docstring (lines 1661-1672) |
| Keys and `--last` | `config/sources.yaml` lines 1001-1003, 1009, 1095-1096; `cli.py` `ingest`/`transform`/`pipeline` options |
| "The 16 October 2026 (current) table keeps every 8 October row unchanged" | Polars on bronze (`dumps.py`): for each dump, 0 keys of the 8 October body missing from 16 October, 0 shared keys with a changed value, 0 full rows missing. NemoLink 15,623 to 16,031 (+408), NSL 17,784 to 17,976 (+192), Viking 19,775 to 20,087 (+312); headers equal; CKAN `last_modified` unchanged (2026-09-17) |
| "Nearly every hour is already past" (Viking) | 19,731 of 19,775 (8 Oct) and 20,062 of 20,087 (16 Oct) targets before the capture |
| NSL cadence "uploads at 10:30 GMT each day, 9 to 16 October 2026" | the 8 new `Data Upload Time GMT` values in the 16 October body: one per day 2026-10-09 to 2026-10-16, `10:30:06` to `10:30:16` |
| NSL "October 2026 files hold day-ahead rows only" | `Auction Type` is `Day Ahead` on every row of both dumps and `DayAhead` on every archive row |
| NSL archive "repeats a row" | archive body 16,632 rows, 16,631 distinct; the 20231029 `DayAhead` `001` `22:00 to 23:00` row twice; `_reconcile_adjudications.json` entry, reconcile log `ADJUDICATED failed nsl` |
| History lines | archive labels: NemoLink weekly 20221012 to 20221216, NemoLink daily archive 20221216 to 20240923, NSL 20221005 to 20240924, Viking 20231229 to 20240924; current tables start 2024-09-25 (NemoLink), 2024-09-24 (NSL, Viking) |
| Member `differs` | headers of each body: current tables carry upload time, auction and `Operational Period Start Date and Time GMT`; archives carry operational date, auction, `Version`, `Hourly Time Period (GMT)`; NemoLink weekly carries one `... GMT/BST ...` label and no auction; intraday carries 24 hour labels and no date |
| "Archive rows add an operational date and version" (Viking) | archive header |
| Related: `historic-demand-data` | NESO dictionary titles "Nemo / North Sea Link / Viking Interconnector Flow" for `NEMO_FLOW`, `NSL_FLOW`, `VIKING_FLOW` (field info `20261008T114228Z`) |
| Related: `interconnector-requirement-and-auction-summary-data` | its note: NESO trades on IFA1, BritNed, NEMO, IFA2, ElecLink and Viking Link; `NEMO Volume` and `VKL Volume` columns (not NSL, so not on the NSL page) |
| Related: `day-ahead-power-exchange-prices-nordpool` (NSL) | its page: GB hourly day-ahead price; the relation stated is only "beside each hour's day-ahead limit" |
| Sibling relations ("with intraday auctions too", "day-ahead rows only", "two more archive tables") | auction values in the bodies; NemoLink has two archives beyond its current table |

## `nemolink` (lead `nemolink_ntc`)

Family page, `held: true`, three members in page-set order. Commands: `pipeline` for `nemolink_ntc` and the weekly
archive; `ingest` only for `nemolink_intraday`, because its transform currently fails (below), so a `pipeline` line
would exit non-zero.

Body corrections (`nemolink.md`):
- Files: "All captures are under .../2026/10/08/" was stale; now names the 8 October captures and the 16 October
  recapture of both dumps, archives skipped (`last_modified` unchanged).
- `nemolink_intraday`: removed "One capture with unchanged metadata does not prove 'not refreshed'"; new "Second
  capture" paragraph: same 24 rows byte-identical, three column ids renamed (`Hourly Time Period GMT`, `Flow in MW To
  GB`, `Flow in MW From GB`), `metadata_modified` 2026-10-09T08:21:47.747573, `last_modified` still empty, transform
  failed with `HeaderEpochError` (gridflow `refresh-20261016/DRIFT.md`), silver keeps the 8 October capture.
- `nemolink_ntc` hold question: counts dated to 8 October, 16 October counts added (16,005 of 16,031 past; 1,684
  before own upload). New "Second capture of the dump" paragraph (file, 1,484,249 bytes, 16,031 rows, append-only,
  408 new rows over 17 upload times, target range, 668 upload times, third silver file). Shape heading dated.
- Cadence: archives did not move on 16 October; intraday renamed; dump upload times mostly 09:30 and 20:11 GMT.

## `nsl` (one table)

One-table held page; three requests (`package_show`, dump, archive). Commands `ingest` then `transform` ("the current
table to silver": the archive is not re-downloaded while its `last_modified` holds).

Body corrections (`nsl.md`):
- Files: "the one capture of each (2026-10-08)" now the 8 October capture of each plus the dump's 16 October capture;
  new "Current dump, second capture" bullet (1,617,906 bytes, 17,976 rows, append-only, 192 new rows, one upload a
  day at 10:30 GMT, still day-ahead only, no target before its own upload, second silver file).
- Activation's "Silver layout: one Parquet file" now one per capture.
- Cadence: "One capture of each resource exists (2026-10-08)" replaced with the two dump captures and the
  append-only result; the TODO now says eight days of appends is not a guarantee.
- Holds item 1: 17,750 / 34 dated to 8 October, 17,951 / 25 for 16 October added.

## `viking` (lead `viking_ntc`)

Family page, `held: true`; lead is the archive (page-set order), then the current table. Commands: `pipeline` per member.

Body corrections (`viking.md`):
- Files: "Each resource has one capture to date, made on 2026-10-08" now: archive one capture, dump two, archive
  skipped on 16 October.
- `viking_link_ntc` "Why it is held": counts dated, 16 October counts added (20,062 of 20,087; 431). New "Second
  capture" paragraph (1,809,697 bytes, 20,087 rows, append-only, 312 new rows over 13 upload times: eight at 09:30,
  three at 16:30, two at 02:30 GMT; 837 upload times; second silver file, `_latest` whole family).
- Cadence: the append-only result added before the TODO.

## Not verified

- The far ends (Belgium, Norway, Denmark) are general facts, as part 1's France. NSL and Viking notes state Norway and
  Denmark; the NemoLink note says NESO's package does not name the far end and only compares with ENTSO-E's GB and
  Belgium border. NESO's own text names none of the three. If the checker wants NESO evidence only, drop the country
  from the NemoLink summary (the budget allows it).
- Whether the 16 October run attempted the archive keys at all (no archive body on 16 October; skip inferred from the
  client rule and unchanged `last_modified` in the family runs that did capture the dumps).
- Dark mode at any width.

## Open questions and template notes

- Manifest leads and members are right. No template problem found.
- The ledger's `nsl` hold text still cites the archive's calendar and `Version`; the archive never loads (repeated
  row), so the page line names the repeat instead. Seat may want the registry hold text to say so.
- NemoLink's `nemolink_intraday` cannot be re-transformed until a second header epoch is frozen; the page shows an
  ingest-only command for it.

## Defects

- NESO, NemoLink: the intraday resource `NemoLink-Intraday1-20240127-001` had three column ids renamed between the 8
  and 16 October 2026 captures (rows unchanged, `last_modified` still empty, `metadata_modified` 2026-10-09); NESO
  announced the 17 September rename only for the current tables. gridflow: the 16 October capture fails
  `HeaderEpochError`; already in `refresh-20261016/DRIFT.md` and the BACKLOG remediation row (12 families), so not
  new; carried for the remediation unit.
- NESO, NemoLink: the package expands NTC two ways ("Net Transfer Capacity" on the title, current and daily archive;
  "NGESO's Network Transfer Capacity" on the weekly archive and the intraday file).
- NESO, NemoLink, NSL, Viking current tables: between the 8 and 16 October 2026 dumps NESO only appended (408, 192,
  312 rows); no row changed. Not proof of immutability; the holds stand. Rows whose target precedes their own upload
  persist (NemoLink 1,684, Viking 431 on 16 October; NSL none).
- NESO, NSL: both dumps and the archive hold only day-ahead rows, though NESO describes day-ahead and intraday
  auctions. Archive repeats one whole row (already adjudicated; carried).
- gridflow / planning: the ledger and registry hold text for `nsl` cite the archive calendar and `Version`, while the
  archive is out on a repeated row (seat item, not a code defect). No gridflow code defect found.
