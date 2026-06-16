"""Agent 4 — Analyst (standard/complex). Extracts figures, computes impact/variance.
Model: Sonnet, or Opus when complexity_flag=True."""
from config import settings
from agents import _llm


def analyst_node(state: dict) -> dict:
    complex_ = bool(state.get("complexity_flag"))
    model = settings.MODEL_OPUS if complex_ else settings.MODEL_SONNET
    if state.get("dry_run"):
        return {
            "extracted_numbers": {"fy28_miia_premium_increase_pct": 6.18},
            "budget_impact_summary": "[dry-run] MIIA premium increase adds an estimated cost above the 2.5% target.",
            "variance_from_forecast": {},
            "analyst_flags": ["exceeds_2.5pct_threshold"],
            "research_flags": [],
            "analyst_model_used": model,
            "routing_path": _llm.append_route(state, "analyst"),
            "pipeline_stage": "analyst",
        }
    prompt_name = "analyst_complex" if complex_ else "analyst_standard"
    system = _llm.load_prompt(prompt_name)
    user = (
        f"document_type: {state.get('document_type')}\n"
        f"budget_thread: {state.get('budget_thread')}\n"
        f"ALG_assumptions: {settings.ALG_ASSUMPTIONS}\n"
        f"memory_context: {state.get('memory_context','')}\n"
        f"raw_body:\n{state.get('raw_body','')[:settings.MAX_BODY_TOKENS*4]}\n"
    )
    out = _llm.parse_json(_llm.call_model(system, user, model, max_tokens=4000))
    out["analyst_model_used"] = model
    out["routing_path"] = _llm.append_route(state, "analyst")
    out["pipeline_stage"] = "analyst"
    return out