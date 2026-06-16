# Acton Finance Agent — Design

## Purpose
Give one time-constrained FinCom member leverage: automatically capture, classify,
analyze, fact-check, and package the flood of Acton municipal + ABRSD budget
communications, anchored to the ALG 2.5%-growth-target work and the budget calendar.

## Pipeline (LangGraph)
Entry is one of two nodes depending on trigger:
- **Email Monitor** (Gmail poll/push) — unread mail from the dedicated agent inbox.
- **Committee Reporter** (nightly) — public Acton/ABRSD/media sites.
Then: **Memory** (retrieve context) → entry → **Supervisor** (classify + route) →
**Deadline Sentinel** (calendar + scenario triggers) → **Analyst** (Sonnet, or Opus
when complex) → **Researcher** (if research_flags) → **Fact-Check** (last gate) →
**Narrative Tracker** → **Savings Agent** (passive gap update) → **Storyteller**
(FinCom memo always for per_item/digest; Town post only for per_item) → **Memory**
(batch write). Noise and fact-check failures short-circuit to the memory-write/end.

See `graph.py` — the edges are a v1 reconstruction from the spec's trigger table.

## Key design rules (from the spec)
- **Classification is narrow:** the Supervisor routes; it never analyzes. Eleven
  document types, eight budget threads, a scored relevance rubric, deadline-aware.
- **Supersession:** for number verification, official_budget_document / capital_plan
  / town_manager_memo are authoritative; minutes / public statements / media are
  narrative-only. Fact-Check enforces this.
- **A figure never reaches the public/FinCom unverified.** Fact-Check is a hard gate;
  arithmetic errors and untraceable figures block.
- **The 2.5% target is tracked municipal-vs-school separately** until the combined
  rollup; the Savings Agent maintains the gap and a 10-point candidate score.
- **Two registers:** FinCom memo (expert, formal) and Town post (plain-English,
  150-250 words, every dollar figure contextualized). Town post excludes open flags.
- **Human-in-the-loop:** attachment downloads, live email sends, and the monthly
  check-in are gated; the agent drafts, Fred approves.

## Models
Haiku for high-volume routing/extraction (Supervisor, Email Monitor, Committee
Reporter, Deadline Sentinel, Narrative Tracker); Sonnet for analysis/synthesis
(Analyst standard, Researcher, Fact-Check standard, both Storytellers, Memory); Opus
for depth (Analyst complex, Fact-Check complex, Savings Agent, Scenario Modeler).

## State
`state/schema.py` — a single `PipelineState` TypedDict. Group 1 = raw entry fields;
Group 5 = the Savings snapshot. Other fields grouped by agent. v1 reconstruction;
reconcile with the design-session grouping.

## Out of scope / deferred
Scenario Modeler is scaffolded but inactive until a milestone trigger is configured
and its prompt Sections 2-6 are drafted. Diligent Community content can't be fetched
automatically (manual access).