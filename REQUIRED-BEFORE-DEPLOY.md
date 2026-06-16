# Required before live deployment

These are the items marked REQUIRED in the prompt-spec review. None block the dry-run
skeleton; all must be resolved before `DRY_RUN = False`. IDs match the review questions.

- [ ] **SUP.1.1** — Supervisor budget-cycle context (gate dates, ALG key assumptions, current FinCom positions, Town Manager name). Target ~June 2026.
- [ ] **EM.1.1 / G.3** — Dedicated agent Gmail account address (forwarding target).
- [ ] **CR.2.1 / G.8** — Current Acton Beacon URL.
- [ ] **AN.2.1** — ALG model key assumption figures (`config.ALG_ASSUMPTIONS`).
- [ ] **AN.2.2** — Current municipal operating budget total (for %-of-budget calcs).
- [ ] **AN.2.3 / SA.2.2** — Prior-year ABRSD assessment (Acton share).
- [ ] **RE.3.1** — Peer municipality list (2-3 comparables).
- [ ] **SF.2.1** — Fred's full name + FinCom title for memo headers.
- [ ] **SF.4.1 / ST.4.1 / G.7** — Acton household count (per-household framing).
- [ ] **DS.2.1** — All budget gate dates for the current cycle (`config.BUDGET_GATES`).
- [ ] **DS.2.2** — ABRSD budget cycle dates (school assessment timeline).
- [ ] **SA.2.1** — Prior-year adopted municipal operating budget baseline.
- [ ] **G.1** — Synology Drive `OUTPUT_ROOT` path on the MacBook.
- [ ] **G.2** — Fred's Gmail for agent notifications / check-ins.

## Deferred / tunable after testing
G.4 MAX_BODY_TOKENS (8000), G.5 COMPLEXITY_TOKEN_THRESHOLD (4000), G.6 thresholds
(PER_ITEM 0.80 / DIGEST_FLOOR 0.40), plus the non-REQUIRED review questions (SUP.1.2,
SUP.3.x, FC.4.x, NT.x, MA.x, SM.x, etc.). The system is designed to be adjusted via
`config/settings.py` without code changes.

## Build-side TODOs (code, not config)
- Gmail client (list/mark-read/send) — `tools/gmail_client.py`
- Web fetch httpx + Playwright + link extraction — `tools/web_fetch.py`
- Document text extraction (PDF/DOCX/XLSX) — `tools/document_tools.py`
- Supabase retrieve + batch write (supersession, content-type validation) — `memory/supabase_client.py`
- Word memo + Excel workbook writers — `tools/docx_writer.py`, `tools/excel_writer.py`
- Deadline Sentinel days-remaining + alert dedupe; monthly Savings check-in email + reply parsing
- Confirm Opus model slug (`claude-opus-4-8` vs spec's `4-7`)
- Review `graph.py` edges and `state/schema.py` group membership against the design session