# entsoe/commercial_schedules: checker review

Checker: Opus 5.5 · high, 2026-09-29. Inputs:
- the canonical note in `vault-p26-entsoe`, diffed against `origin/master` (the mirror matches it byte for byte);
- the artefacts and the built page in `p26-entsoe`, and the writer's report;
- gridflow at `2822d38`, local silver and bronze (read only);
- Elexon `fuelhh` silver (read only) and the ENTSO-E code list.

## Verdict: REVISE

There is 1 blocker, 1 major and 5 nits.

The writer's hard findings stand, and I reproduced each one:
- the `A01`/`A05` collapse;
- the direction check;
- the chart values;
- the commands and the request URL.

The fixes are field edits only. No re-distil is needed, because the chart spec is unchanged.

## Findings

1. **blocker: `page.facts.grain`**
   - **What is wrong.** The grain reads "One row per interval start, `in_Domain` zone and `out_Domain` zone". That is three columns. The code's uniqueness is four columns, and the page's own Key line, directly beneath it, lists four. So the grain claims a uniqueness gridflow does not guarantee.
   - **Why the writer's reason does not hold.** The writer left `business_type` out because it is constant `A06` in the rows we hold. That makes the grain a measured-on-our-copy universal, which rubric §1 disallows. If ENTSO-E sent a second `businessType` for a pair, silver would keep both rows and the grain line would be false. The code allows for exactly that.
   - **Evidence.**
     - Dedup `unique(subset=["timestamp_utc", "in_area_code", "out_area_code", "business_type"], keep="last")` at `gridflow/silver/entsoe/h6_market.py:91-98`.
     - `business_type` is the only other column the transformer writes, `h6_market.py:107-117`.
     - Silver `business_type.unique()` returns `['A06']`: constant, but by observation, not by rule.
   - **Fix.** "One row per interval start, `in_Domain` zone, `out_Domain` zone and `businessType`" (11 words, fact budget 14).

2. **major: `page.chart_view.key[belgium].note`**
   - **What is wrong.** "Tracks the import part of Elexon's INTNEM (project check)" overclaims. In the window drawn, Belgium often shows a sizeable schedule into GB while INTNEM is not importing. That is the pilot's overclaim class ("the same flow").
   - **Evidence.** Hourly means of `fuelhh` INTNEM, the latest `published_at` per period, joined to silver rows with `in_area_code` GB and `out_area_code` BE:
     - 14 to 20 Sep (the chart): a schedule above 200 MW while the INTNEM import part is below 50 MW in 49 of 168 hours;
     - 1 Aug to 21 Sep: the same in 106 of 456 hours;
     - correlation with `max(INTNEM, 0)`: 0.855 in the chart window, 0.860 over the range.
   - **France is different.** FR (INTFR + INTIFA2 + INTELEC) disagrees in only 8 of 168 chart hours, with correlation 0.93 to 0.95. "Tracks" is defensible there. Softening it the same way is optional.
   - **Fix.**
     - Something like "Moves with Elexon's INTNEM imports (project check), not hour for hour; zero for 11 hours on the 17th." (18 words, key-note budget 18).
     - Keep correlation figures off the page (rubric §3). They belong in the vault body.

3. **nit: `page.what_it_is` (the day-ahead loss)**
   - **What is wrong.** The seat asked that the page say plainly that the day-ahead series is lost. The page says gridflow "drops the contract type and keeps the one listed last, `A05`". The loss is implied, not stated.
   - **Evidence (reproduced from bronze).**
     - All replies for 1 to 5 Aug and 8 to 21 Sep, 8 pairs x 21 days: 7 pairs list `(A01, A05)` in every reply, and GB to IE-SEM lists `(A05,)` only.
     - The parser has no branch for the payload tag `contract_MarketAgreement.type` (`gridflow/connectors/entsoe/parsers.py:320-328`).
     - I reparsed the bronze with the contract type kept and joined it on the key: 9,110 of 9,110 silver `quantity_mw` equal the `A05` value. 2,755 also equal `A01`, where the two coincide.
     - The share of rows where `A01` differs from `A05` is 23 to 97 per cent per pair.
   - **Fix.** Combine with finding 4 in one sentence, for example: "A reply can hold a day-ahead series (`A01`) and an `A05` series (total, in ENTSO-E's code list); gridflow drops the contract type and keeps `A05`, listed last (project check), so the day-ahead series is lost." The whole field is then 59 words (budget 60).

4. **nit: `page.what_it_is` ("total in the entsoe-py client's reading") and the note body's Known issues ("no ENTSO-E quote recorded")**
   - **What is wrong.** A vendor source exists, so the hedge attributes the meaning to the wrong source.
   - **Evidence.**
     - ENTSO-E Code Lists, version 29 release 0, section 3.8 `ContractTypeList`, gives `A05` as "Total", defined as "This is the sum of all capacity contract types for the period covered". `A01` is "Daily" (allocation by daily auction).
     - Source: https://eepublicdownloads.azureedge.net/clean-documents/EDI/Library/Core/entso-e-code-list-v29r0.pdf
   - **Keep it scoped.**
     - This is ENTSO-E's generic EDI code list, not the Transparency Platform's A09 guide. Cite it as the code list.
     - It does not license "`A05` = `A01` plus more". The writer found `A05` below `A01` on FR to DE-LU, so the page must not say that.
   - **Fix.**
     - Page: cite "ENTSO-E's code list", as in finding 3.
     - Body: replace "no ENTSO-E quote recorded" with the code-list definition and its citation.

5. **nit: `page.record.fields.quantity_mw`**
   - **What is wrong.** "MW of the `A05` series" is unscoped. What silver holds is the last-listed series. It is `A05` only because of the vendor's element order in these replies (finding 3), and a future reply order would change it. The neighbouring `business_type` line scopes itself with "here".
   - **Fix.** "MW of the last-listed series, `A05` here; A03 points repeat until the next" (13 words, meaning budget 14).

6. **nit: `page.chart_view.alt` (Belgium clause)**
   - **What is wrong.** "Belgium moves between zero and 1,055 MW, peaking at 660 MW on the 17th" reads as if 660 MW were the series peak.
   - **Evidence.** Silver, `in_area_code` GB and `out_area_code` BE, 14 to 20 Sep: the series maximum is 1,055 MW (14th); 660 MW is the 17th's maximum.
   - **Fix.** "…between zero and 1,055 MW, and reaches 660 MW at most on the 17th."

7. **nit: vault body, Known issues, direction bullet ("correlation 0.85 to 0.94 per border")**
   - **What is wrong.** The construction is not named, and it matters for IE-SEM:
     - the positive part of the summed flow (`max(INTEW + INTIRL + INTGRNL, 0)`) gives 0.853, which reproduces the note;
     - the sum of each link's positive part gives 0.792.
   - FR 0.925, BE 0.860 and NL 0.940 reproduce under either construction, over 1 Aug to 21 Sep, hourly.
   - **Fix.** Say "the positive part of the summed Elexon flows, hourly".

## Checked and correct

- **Request.** `raw_feed.requests` matches the bronze sidecar `2026/09/16/raw_20260926T181933Z_d821d778.meta.json` `request_url`: parameter order, no `processType`, no contract filter.
- **Direction.** `in_Domain` as the receiving zone is worded as a project check everywhere on the page (`what_it_is`, `record.fields.in_area_code`, the key notes). It is never presented as an ENTSO-E rule. `_FLOW_PAIRS` (`connectors/entsoe/client.py:40-49`) has no reverse pairs, so "exports from GB are not drawn" is a code fact.
- **Commands.**
  - `day_subwindows` treats the end as exclusive (`utils/time.py:123-147`), so ingest `--end 2026-09-21` fetches up to the 20th.
  - `PARTITION_SOURCE_OFFSETS` keeps the default `(0,)` (`silver/base.py:417`), with no override on `CommercialSchedulesTransformer`.
  - The transform `--end` is inclusive.
- **Point time.** `timestamp_utc` is "period start plus (position minus 1) times resolution", matching `parsers.py:530` and `:582`.
- **Cadence.**
  - The cadence reads "as sent in the responses we hold", per ruling #39.
  - The `resolution` guide scopes `PT60M`/`PT15M` with "here". Silver agrees: the four GB pairs are `PT60M`, and the four continental pairs are `PT15M`.
  - Every bronze curve is `A03`.
- **`published_at`.** It is described as a fetch-time stamp, per ruling #39.
- **Chart.**
  - The committed series has `spec_origin: vault`, 4 series x 168 hourly points, and 0 mismatches against silver point by point.
  - Every number in the alt and the key notes matches silver:
    - FR: maximum 3,076, at or above 3,000 MW for 5 to 10 hours on each day but the 19th, 1,979 MW at most on the 19th, and a daily minimum below 210 every day;
    - BE: 11 zero hours on the 17th;
    - NL: 410 MW on the 19th and 1,172 MW on the 20th;
    - IE-SEM: maximum 280.827, non-zero only on the 14th, 16th and 17th.
  - No staged spec and no authored override exist.
- **Frame.** `gridflow-sample` produced 8 real rows at 16 Sep 21:00 UTC, one per ordered pair.
- **Notebook.**
  - The cells are read-only and the outputs have no errors.
  - The `query()` end is inclusive via `_date_range_predicate` (`gridflow_models/research/handles/source.py:437-449`).
  - `plot_alt` matches the plot.
- **Related.** The four related notes are accurate and 12 words or fewer.
- **Build and detector.**
  - `gridflow-build --only entsoe/commercial_schedules` passes.
  - `detect.mjs` returns only the accepted `em-dash-overuse` advisory from EIC padding (ruling #39/#40). The rendered prose has no dashes, arrows or middle dots.
- **No local data on the page**, beyond the ruled cadence phrase.
- **Screenshots.**
  - I used my own CDP script with static server port 9819, at 1440, 1024, 768 and 390, with the frame and notebook both folded and unfolded.
  - Nothing is clipped or overlapping: hero turbines, chart axes, the four-entry key, request, commands, frame, guide, notebook panel and image, related links, and every corner label.
  - Dark equals light, because the site has no dark scheme.
  - The known `.ipynb` tab clip at 390 is seat work.
  - The server is stopped, with no listeners on 9819 or 10819.
