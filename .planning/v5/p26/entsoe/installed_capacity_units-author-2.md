# installed_capacity_units: writer response to review 1

Writer: Opus 5.5 (high), 2026-09-29. Answers `installed_capacity_units-review.md` (REVISE: 1 major, 3 nits). Every finding is fixed in the canonical note (`vault-p26-entsoe/30-vendors/entsoe/datasets/installed_capacity_units.md`), and the mirror is byte-identical (`cmp`).

## Fixes

| # | Finding | Field | Now reads |
|---|---|---|---|
| 1 (major) | Observed behaviour stated as a rule | `page.what_it_is` | "... gridflow asks per UTC day; the replies received each carried the whole year, so silver holds one copy per fetch, told apart by `published_at`." (60 words; the ambiguous "Each ingest day" is gone.) |
| 1 (major) | same | `page.notebook.lead` | "... filtered on `timestamp_utc` with both ends included; lineage columns are dropped. In the replies received each fetch added a full copy, so keep each unit's latest `published_at`." (33 words; "(the year start)" was dropped to fit, and `fields.timestamp_utc` still gives it.) |
| 2 (nit) | B08 "peat" has one source | `page.chart_view.key[smaller].note` | "B08 peat per entsoe-py (IE-SEM's West Offaly, Edenderry, Lanesboro), with marine, solar, waste and storage." The note body's `production_type` schema row now names the three B08 units and states the entsoe-py-only basis. |
| 3 (nit) | "many" rests on a local overlap | `page.related[entsoe/actual_generation_units].note` | "Output per unit, keyed on the same kind of unit EIC (`unit_mrid`)" |
| 4 (nit) | Sample `ingested_at` earlier than `published_at` | Body, "Silver sample" | `"ingested_at": "2026-09-15T20:09:28.630326+00:00"`, the real value for the ABRBO row in `installed_capacity_units_20260914.parquet` |
| Checker's wording point | "365 identical requests" | Body, Known issues, "One day is enough" | "about 365 requests per zone (differing only in `periodStart`/`periodEnd`); if each returns the same document, as all replies seen so far did, that is 365 silver copies." |

Evidence for fix 2: in silver, `production_type == "B08"` holds exactly three units, all `10Y1001A1001A59C`: `47W000000000170O` West Offaly Production (135 MW), `47W000000000159C` Edenderry Prod (118) and `47W000000000232S` Lanesboro Production (91).

## Gates

- The chart spec is unchanged, so there was no re-distil. The sample and notebook cells are unchanged, so their digests still match. The lead is page words only.
- `uv run --system-certs --extra build gridflow-build --only entsoe/installed_capacity_units` wrote the page. No budget, digest or related errors.
- `node C:/Users/Bobbo/OneDrive/Desktop/Python/gridflow-front-end/.claude/skills/impeccable/scripts/detect.mjs --json` gives one `em-dash-overuse` advisory (92 hits, from EIC `--` padding; accepted under ruling #39).
- Rendered page:
  - 0 real em dashes;
  - "Each ingest day" and "many of its" are gone;
  - all four new phrasings are present;
  - no literal `---` in the front matter.
- Screenshots (`file://`, every Chrome call inside `timeout 60`, no server started; port 9670 not touched):
  - the key at 1024 (the narrowest key column) and at 390;
  - the new B08 note wraps over three lines at 1024, with nothing clipped.
- No git. No files outside this dataset's were touched.

Summary: I fixed all four review findings (the scope major, the B08 provenance, the related wording and the sample `ingested_at`) plus the checker's "365 identical requests" wording point; the mirror is identical, the `--only` build is clean, and the detector shows only the accepted advisory.
