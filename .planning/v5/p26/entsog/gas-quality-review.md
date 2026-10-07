# entsog/gas-quality: review

Checker: Sonnet 5.5 · high, 2026-10-07. Family `gas-quality`, lead `gcv` (members `wobbe_index`, `methane_content`, `hydrogen_content`, `oxygen_content`). Inputs: the five canonical notes diffed against `origin/master` in the vault worktree, the committed series, sample and notebook, the page rebuilt with `gridflow-build --only entsog/gcv`, gridflow code, local silver and bronze (read only), screenshots on port 9894.

## Verdict: REVISE

Two majors, seven nits, no blockers. The page's facts, chart, units and request URLs all reproduce. The majors are one omission on the page (the placeholder rows' stamps) and one false sentence in the vault body (the repeated-values note). Both are short fixes. The author's ship recommendation stands once they are made.

## What I reproduced (all agree with the page)

- **Build and detector.** `gridflow-build --only entsog/gcv` succeeds (28 generic "no Pydantic class" warnings only; wrote `data-sources/entsog/gas-quality.html`). `detect.mjs --json` returns `[]`. No staged chart spec and no authored override exist. Mirrors: `cmp` byte-equal for all five notes. Series `spec_origin: vault`, digest check passes.
- **Chart.** Recomputed from silver: Moffat (IE) entry 11.87, 11.83, 11.76, 11.82, 11.79, 11.80, 11.82, 11.83, 11.84; National Gas TSO exit 11.6429 for 13 to 18 Sep, then 11.6927, 11.6136, 11.5902 (rounded 11.643, 11.693, 11.614, 11.59); Interconnector entry 11.645 for 13 to 18 Sep, then 11.673, 14.253, 11.602. All match `series/entsog/gcv.json`, the alt text and the key notes. Provenance: 42 rows matched (14 days × 3 operators), 27 used (9 days × 3). The `value > 0` filter drops exactly Interconnector's 14 zero exit rows (no other zero exists in `entsog/gcv`) and the 42 null placeholders; the caption says both. Axis carries one unit, `kWh/Nm3`.
- **20 Sep outlier.** Interconnector `UK-TSO-0003` ITP-00005 entry GCV 14.253 (`Confirmed`, `lastUpdateDateTime` 2026-09-21 08:48:29 UTC) against National Gas TSO 11.6136 (gap 2.6394; every other gap is 0.0021 to 0.0197). Interconnector's own Wobbe index that day is 14.901; (GCV/Wobbe)² = 0.9149, against 0.6229 to 0.6346 on its other 13 days. The page does not speculate on a cause (see finding 3 for how plainly it flags it).
- **No silver loss.** Bronze records against silver rows: gcv 98 to 98 (56 valued to 56), wobbe_index 126 to 126 (28 to 28), methane_content 42 to 42, hydrogen_content 28 to 28, oxygen_content 28 to 28; one bronze file per gas day, 14 days each. `meta.count`/`meta.total`: gcv 7/8, wobbe_index 9/9, methane 3/6, hydrogen and oxygen 2/4. Every record is one day long (`period_to - period_from` = 1 day), so the day partition keeps all of them; the held capacity page's loss does not apply. No use named in `how_used` is something silver cannot deliver.
- **Units and wording.** `unit` is `kWh/Nm3` on every gcv and wobbe row and `% (mol/mol)` on every methane, hydrogen and oxygen row; `generic.py:189-191` casts `value` to Float64 with no conversion. The response (bronze `fields` and rows) carries no reference conditions, so "the response states no reference conditions" is true.
- **Grain and key.** 0 duplicate `(timestamp_utc, operator_key, point_key, direction_key)` groups in all five tables; dedup is on the vendor `id`, `keep="last"` (`generic.py:193-199`); `timestamp_utc` is a copy of `period_from` (`generic.py:185-187`).
- **Requests.** `raw_feed.requests` and every `family.members[].request` equal the `request_url` in each member's bronze `.meta.json` for 2026-09-21 (including `indicator=Wobbe+Index` and the `%2C` encoding). Commands match the approved nominations page; no `PARTITION_SOURCE_OFFSETS` exist for entsog.
- **Other facts.** "Provisional throughout" holds for GNI and National Gas TSO on all 14 days. Placeholder remarks quoted in the notes match silver exactly. `lastUpdateDateTime` lags (GNI 25.1 to 28.6 h, Interconnector 28.6 to 51.8 h, National Gas TSO 83.9 to 133.0 h) match the note. Interconnector's exit is 0.0 on all 14 days in all five members. Wobbe flat 14.653 on 13 to 19 Sep, methane 85.39, hydrogen 0.005 on 13 to 18 Sep: confirmed.
- **Rubric greps** (`locally`, `held`, `our`, `since 20`, `% of`, `live`, `now`, `yet`, `soon`, `planned`, `coming`, real-time, digits plus `rows`/`days`, em dash, arrow, middle dot) on the rendered text: nothing.
- **Screenshots** (taken by me): 1440 (four views), 1024, 768 (two views), 390 in a true 390 px iframe (hero, chart, frame, notebook). Nothing clipped or overlapping; no horizontal overflow at 390. Unfolded frame (checkbox forced on): the table scrolls inside its box, same as the approved template. Notebook output cells in the JSON have no errors; the committed `gcv-5.png` matches `plot_alt`.

## Findings

### 1. major · `page.record.fields.timestamp_utc` (and the key and grain lines) · placeholder rows' earlier stamps are not stated

The guide says "Start of the gas day, from the vendor `periodFrom`, in UTC". That is true of valued rows only. The not-applicable placeholders send an earlier `periodFrom`, so their `timestamp_utc` is not a gas-day start, and nothing on the page says so. The eight rows shown are all valued rows, so the frame cannot show it; the notebook's `query()` does return the placeholders.

Evidence (silver, Polars, `timestamp_utc` hour of day):
- `entsog/gcv`: 56 rows at 04:00 UTC (valued), 42 rows at 03:00 UTC (all placeholders).
- `entsog/wobbe_index`: 28 at 04:00, 70 at 03:00, 28 at 02:00 (GNI's placeholders).
- Bronze: placeholder `periodFrom` `2026-09-21T05:00:00+02:00` (GNI wobbe `04:00:00+02:00`), valued rows `06:00:00+02:00`.

The vault body states this ("Two `timestamp_utc` values per gas day", "Three ... per gas day"); the page does not. Under the seat's ship-or-hold ruling, "wrong stamps" is a hold reason unless the page says plainly what silver does. The page ships, so it must say it.

Fix: in `record.fields.timestamp_utc`, say valued rows carry the gas-day start and placeholders an earlier `periodFrom`, within 14 words (for example "Gas-day start from `periodFrom`, in UTC; placeholders send an earlier one"). Keep it as sent in the responses; no counts.

### 2. major · vault body, `gcv.md` "Repeated values" (and the author report) · "each with its own `lastUpdateDateTime`" is false for National Gas TSO

The note says National Gas TSO sends 11.6429 on six consecutive gas days, "each with its own `lastUpdateDateTime` (re-sent values, not one repeated record)". Silver, National Gas TSO ITP-00005 exit (UTC):

| gas day | value | `last_update_date_time` |
|---|---|---|
| 13 Sep | 11.6429 | 09-16 15:54:49 |
| 14 Sep | 11.6429 | 09-18 15:54:29 |
| 15 Sep | 11.6429 | 09-18 15:54:29 |
| 16 Sep | 11.6429 | 09-19 15:53:50 |
| 17 Sep | 11.6429 | 09-22 16:01:49 |
| 18 Sep | 11.6429 | 09-23 17:02:50 |
| 19 Sep | 11.6927 | 09-23 17:02:50 |
| 20 Sep | 11.6136 | 09-23 17:02:50 |

The 14th and 15th share one stamp, and the 18th to 20th share another (the 18th's flat value and the 19th and 20th's changed values were updated at the same instant). So "each with its own stamp" fails for two of the six days, and "re-sent values, not one repeated record" is not supported for this operator. Interconnector's seven wobbe/gcv stamps (13 to 19 Sep) are distinct, so the sentence holds for Interconnector. The page does not repeat the claim (its key note says only "11.643 on six days running", which is true).

Fix: in `gcv.md` Known issues, scope the clause to Interconnector, and for National Gas TSO say the stamps are shared on 14 and 15 Sep and on 18 to 20 Sep, or drop the "re-sent, not one record" inference. Correct the same sentence in the author report if it is reused.

### 3. nit · `page.chart_view.key[bacton_iuk_entry].note` · the 20 Sep value could be flagged more plainly

"within 0.02 of National Gas TSO's except 14.253 on the 20th" is true and speculates on nothing, but it does not say the figure is as Interconnector sent it (`Confirmed`), and it reads slightly as if the exception belonged to National Gas TSO's series. A reader of a spike with no label on the chart cannot tell a vendor value from a gridflow fault. The page's only other cue is the notebook plot, where GCV rises to meet the Wobbe line.

Suggestion (still within the note's room): "Interconnector's report, `Confirmed`; within 0.02 of National Gas TSO's except 14.253 on the 20th, as sent."

### 4. nit · `page.chart_view.key[bacton_iuk_exit].note` and the chart · the National Gas TSO line is hidden for six of nine points

The two Bacton (IUK) series differ by 0.0021 on 13 to 18 Sep, so the later-drawn Interconnector line covers National Gas TSO's; the screenshots show one orange line over the teal one until the 19th. The key note ("11.643 on six days running") mitigates it, and the author already reported it as a renderer matter. No page change needed; listed so the seat can decide whether the renderer offset is worth doing.

### 5. nit · `page.family.members[hydrogen_content|oxygen_content|methane_content].differs` · exit zero not mentioned, and "only" is unscoped

"only Interconnector reports, at Bacton (IUK) entry and exit" suggests the exit carries data; in silver it is 0.0 on every row of all five members (the `value` guide mentions Interconnector's exit zero for GCV only). Also, "only ..." for these members is an observation about what the nine filters return (the other filters return no record at all, so no vendor remark documents the absence), stated without scope. For wobbe_index the "only" is backed by the operators' own placeholder remarks, so it is fine.

Suggestion: "Hydrogen in `% (mol/mol)`; Interconnector at Bacton (IUK) entry, its exit sends 0" and the same for oxygen; for methane add GNI as now and the exit zero if the 14 words allow.

### 6. nit · `page.what_it_is` / vault body · the register lists declared GCV units that differ by operator

The author's report says nothing in "the rows, the vault or the code" states reference conditions. The response itself indeed does not, and the page says only that. But the related register (`entsog/operator_point_directions`, silver columns `tp_tso_gcv_unit`, `tp_tso_gcv_remarks`) carries a GCV unit per point direction that differs by operator at the points compared in `how_used` 1: National Gas TSO ITP-00005 exit `MJ/Sm3` (min 39.0); Interconnector ITP-00005 entry and exit `kWh/Nm3` (min 11.5); BBL company `kWh/m3(n)` (9.6 to 9.9); GNI Moffat `kWh/Nm3` with a remark citing ISO 13443:1996. The operationalData rows label both Bacton reports `kWh/Nm3` and they agree within 0.02, so the comparison is empirically sound, but the page invites a cross-operator reading without noting the register. This is a missed domain fact, not a false statement.

Suggestion: add one sentence to the gcv note's body (Known issues) pointing at the register's declared units; the page can stay as is.

### 7. nit · `page.notebook` and sample frame at 390 px · the value column sits behind the fold

At 390 the frame shows only `timestamp_utc` before the `…` fold, so the column that matters (`value`) needs the unfold tap. This is the template's width tiers with four key columns first, the same as the approved nominations page; no author change. Listed for the seat only.

### 8. nit · `page.summary` · "at Bacton and Moffat" is unscoped across the five indicators

Wobbe index, hydrogen and oxygen have values only at Bacton (IUK) in the responses; GNI's Moffat Wobbe rows are placeholders ("GCV published", "n/a"). The `differs` lines say so, but the summary is read first. Suggestion: name Bacton and Moffat only for GCV and methane, or drop the places from the summary.

### 9. nit · `page.record.fields.is_cmp_relevant` · abbreviation not expanded, unlike the approved sibling

Nominations says "Vendor flag for congestion management procedure (CMP) relevance, as sent"; here it is "Vendor CMP relevance flag, kept as text because placeholders send it empty". Expand CMP once, keep the text-dtype reason.

## Not verified

- Why 14.253, why the repeated runs, what `meta.total` counts, and what Interconnector's exit zero means: the author left all four open and the page claims none of them.
- The vendor's reference conditions for `kWh/Nm3`: no vendor document in the notes states them.

## Defects to log (beyond the author's list)

- **[vendor data, observation] National Gas TSO's `lastUpdateDateTime` is shared across gas days.** `entsog/gcv`, UK-TSO-0001 ITP-00005 exit: gas days 14 and 15 Sep 2026 both 2026-09-18 15:54:29 UTC; gas days 18, 19 and 20 Sep all 2026-09-23 17:02:50 UTC. The value changes between the 18th and the 19th at the same stamp, so the stamp is a batch time, not a per-value revision time.
- **[vendor data, observation] The register declares different GCV units from the operationalData unit label.** `silver/entsog/operator_point_directions`: `tp_tso_gcv_unit` `MJ/Sm3` for UK-TSO-0001 ITP-00005 exit against `kWh/Nm3` in `entsog/gcv` rows for the same point direction. Worth a vendor or register check before any cross-operator model uses GCV.
