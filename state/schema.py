"""Pipeline state for the Acton Finance Agent LangGraph.

v1 RECONSTRUCTION from the prompt spec doc — every field below is referenced by an
agent's input/output section. The "Group" comments mirror the doc's references
(Group 1 = raw entry fields; Group 5 = savings snapshot). Group membership beyond
1 and 5 was inferred — review and adjust.
"""

from __future__ import annotations
from typing import TypedDict, Any


class PipelineState(TypedDict, total=False):
    # --- Group 1: raw entry (Email Monitor / Committee Reporter) ---
    raw_sender: str
    raw_subject: str
    raw_body: str
    raw_url: str
    trigger_type: str          # "email" | "scheduled_poll"
    source: str
    received_at: str           # ISO 8601
    attachments: list[dict]    # metadata only (no download)

    # --- Supervisor classification ---
    document_type: str         # one of eleven types
    budget_thread: str         # one of eight threads
    relevance_score: float
    complexity_flag: bool
    gate_type: str             # per_item | digest | no_gate
    classification_reasoning: str

    # --- routing / meta (every node appends) ---
    routing_path: list[str]
    pipeline_stage: str

    # --- Analyst ---
    extracted_numbers: dict[str, Any]
    budget_impact_summary: str
    variance_from_forecast: dict[str, Any]
    analyst_flags: list[str]
    research_flags: list[dict]
    analyst_model_used: str

    # --- Researcher ---
    research_findings: list[dict]
    sources_consulted: list[str]

    # --- Fact-Check ---
    fact_check_passed: bool
    fact_check_flags: list[str]
    fact_check_model_used: str
    verification_summary: str
    resolution_required: str

    # --- Storyteller (both registers) ---
    draft_fincom_memo: str
    draft_town_post: str
    output_register: str       # "fincom" | "town"
    output_file_paths: dict[str, str]   # e.g. {"excel": "...", "docx": "..."}

    # --- Deadline Sentinel ---
    active_deadlines: list[dict]
    sentinel_notes: list[str]
    scenario_modeler_triggered: bool

    # --- Narrative Tracker ---
    narrative_flags: list[dict]

    # --- Group 5: Savings Agent snapshot ---
    municipal_gap_dollars: float
    school_gap_dollars: float
    combined_gap_dollars: float
    residual_gap_dollars: float
    top_candidates: list[dict]
    savings_last_updated: str
    last_checkin_at: str
    pending_override_reviews: list[dict]
    checkin_report_sent: bool
    checkin_email_subject: str

    # --- Scenario Modeler (stub; add before activating) ---
    scenario_analysis: dict[str, Any]

    # --- Memory Agent ---
    memory_context: str
    memory_sources_retrieved: list[str]
    memory_writes: list[dict]          # queue filled by agents during the run
    memory_writes_executed: int
    memory_writes_failed: int
    memory_write_errors: list[str]

    # --- control ---
    dry_run: bool


def new_state(**kwargs) -> PipelineState:
    """Fresh state with sane defaults for list/dict fields."""
    base: PipelineState = {
        "routing_path": [],
        "memory_writes": [],
        "analyst_flags": [],
        "research_flags": [],
        "narrative_flags": [],
        "active_deadlines": [],
        "sentinel_notes": [],
        "extracted_numbers": {},
        "variance_from_forecast": {},
        "output_file_paths": {},
        "dry_run": True,
    }
    base.update(kwargs)  # type: ignore[arg-type]
    return base