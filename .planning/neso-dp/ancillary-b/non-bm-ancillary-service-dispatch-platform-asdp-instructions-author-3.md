# ASDP dispatch instructions: writer round 3 (2026-10-23)

Follow-up from the OBP reserve instructions check. The page said the ASDP services "moved" to OBP, but ASDP silver holds
only `Non-BM STOR`, `Non-BM Fast Reserve` and `RDP_NEGATIVE` rows. OBP's rows are Positive Quick Reserve, Positive Slow
Reserve and MW Dispatch, from 10 October 2025, and NESO's OBP text says OBP will "incrementally" master more non-BM
services. Edited in the canonical note only (CRLF kept on all 571 lines) and mirrored (`cmp` clean). Build
`--only neso_data_portal/asdp_instructions` ok, detector `[]`, 0 em dashes, and "moved" no longer appears on the page.
The chart spec, sample and notebook did not change. Screenshot: `asdp-instructions-shots\r3-asdp-instructions-hero-related.png`
(hero facts at 1440 and 390, related list at 390): nothing clipped. My 9983 server is stopped.

| Field | Was | Now |
|---|---|---|
| `page.related[1].note` | "Non-BM reserve instructions on OBP, where these moved; never join ids" | "OBP, the platform NESO is moving non-BM services to; never join ids" |
| `page.facts.cadence` (same claim, so I counted it as a matching line) | "NESO lists it as not active: the services moved to its Open Balancing Platform" | "Not active (NESO's label); NESO is moving non-BM services to its Open Balancing Platform" (cut to fit 14 words) |
| Body, overview heading | "ASDP has been superseded by OBP, and the two overlap in time." | "NESO is moving non-BM services from ASDP to OBP, and the two overlap in time." The quote of this package's own text ("have now migrated to the OBP system") stays, because NESO does say that |
| Body, Known issues "Migration to OBP" (the line describing OBP's vendor text) | "...says some non-BM instructions are still published on ASDP..." | "...says OBP will incrementally master more non-BM services, with less published on ASDP...", plus one sentence: ASDP silver holds only `Non-BM STOR`, `Non-BM Fast Reserve` and `RDP_NEGATIVE` rows, while OBP's rows, from 2025-10-10, are Positive Quick Reserve, Positive Slow Reserve and MW Dispatch (linked to the OBP instructions note). The TODO on the two vendor statements stays open |

NESO's service names: the page itself names no OBP service now (the related note names only the platform). The body
uses NESO's names, as the OBP instructions note decodes them: Positive Quick Reserve (`PQR`), Positive Slow Reserve
(`PSR`), MW Dispatch (`RDP`).

Evidence: OBP instructions note (vault worktree), lines 140 to 155: vendor text "OBP will incrementally master more
non-BM services as they migrate", the decoded service names, and that ASDP's Fast Reserve and STOR instructions "are
**not** in this file". ASDP silver `service_type` values: `Non-BM Fast Reserve` 72,503, `Non-BM STOR` 1,620,
`RDP_NEGATIVE` 14 (round 1).

No other changes.
