# Acton Finance Agent

A municipal-finance monitoring pipeline for a member of the **Acton, MA Finance
Committee**. It watches town and school-district communications (email + public
websites), classifies and analyzes anything budget-relevant against the ALG
multi-year forecast, fact-checks every figure, and drafts a FinCom memo (and, when
warranted, a plain-English town post). Built as a **LangGraph** pipeline of 13
Anthropic-model agents, with a Supabase memory store, designed to run on a MacBook
with output to Synology Drive.

> This is the build scaffold (first commit). It runs end-to-end in **dry-run** on
> mock data today; live operation needs the items in `REQUIRED-BEFORE-DEPLOY.md`.

## Architecture at a glance
`docs/DESIGN.md` has the full picture. The 13 agents:

Supervisor (routes) · Email Monitor + Committee Reporter (entry points) · Analyst
(standard/complex) · Researcher · Fact-Check (the last gate before drafting) ·
Storyteller (FinCom memo + Town post) · Deadline Sentinel · Narrative Tracker ·
Savings Agent (the 2.5%-target gap tracker) · Memory Agent (shared service) ·
Scenario Modeler (stub, not active).

Models: Haiku (`claude-haiku-4-5-20251001`), Sonnet (`claude-sonnet-4-6`), Opus
(`claude-opus-4-8` — the spec said 4-7; confirm). Set in `config/settings.py`.

## Layout
```
acton-finance-agent/
├── main.py            # run one pass (dry-run on mock data)
├── scheduler.py       # APScheduler: nightly reporter, email poll, (todo) daily sentinel + monthly check-in
├── graph.py           # LangGraph wiring (v1 reconstruction — review)
├── config/settings.py # all tuning, maps, model slugs, placeholders
├── state/schema.py    # pipeline state (v1 reconstruction — review)
├── agents/            # the 13 agent nodes (+ _llm.py helper)
├── prompts/           # 14 system-prompt files (your drafts; [PLACEHOLDER]s intact)
├── tools/             # gmail, web_fetch, document, docx/excel writers (stubs)
├── memory/            # supabase_client + savings_store (stubs)
├── tests/mock_data/   # sample_email.json, sample_agenda.html
└── docs/DESIGN.md
```

## Run it (dry-run)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # fill in when going live
python main.py              # email entry, mock data
python main.py --reporter   # committee-reporter entry, mock data
```
Dry-run uses mock data and stubbed integrations — no API calls, no Supabase, no
Gmail. Flip `DRY_RUN = False` in `config/settings.py` only after the REQUIRED items
are filled and the integration stubs (marked `[TODO]`/`NotImplementedError`) are
implemented.

## Status of the build
- ✅ Repo structure, config, state, graph wiring, all 13 agent nodes, all 14 prompts, mock data — runs in dry-run.
- 🔲 Integrations are stubs: Gmail, web fetch (httpx/Playwright), document parsing, Supabase, Word/Excel writers.
- 🔲 19 deployment items in `REQUIRED-BEFORE-DEPLOY.md` (dates, baselines, household count, URLs, accounts).
- 🔲 `graph.py` + `state/schema.py` are reconstructed from the spec — review the wiring and field groups.

## Notes
- No secrets in the repo (`.gitignore` covers `.env`, credentials, tokens). PHI is
  not in scope here, but treat resident/communication data carefully.
- The FinCom memo is produced as plain text by the Storyteller and converted to Word
  by `tools/docx_writer.py`.