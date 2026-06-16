"""Agent 6 — Fact-Check. Verifies arithmetic, sourcing, supersession. Last gate before drafting.
Model: Sonnet, or Opus when complexity_flag=True."""
from config import settings
from agents import _llm


def fact_check_node(state: dict) -> dict:
    model = settings.MODEL_OPUS if state.get("complexity_flag") else settings.MODEL_SONNET
    if state.get("dry_run"):
        return {
            "fact_check_passed": True,
            "fact_check_flags": [],
            "fact_check_model_used": model,
            "verification_summary": "[dry-run] all figures verified.",
            "routing_path": _llm.append_route(state, "fact_check"),
            "pipeline_stage": "fact_check",
        }
    system = _llm.load_prompt("fact_check")
    user = (
        f"extracted_numbers: {state.get('extracted_numbers',{})}\n"
        f"budget_impact_summary: {state.get('budget_impact_summary','')}\n"
        f"variance_from_forecast: {state.get('variance_from_forecast',{})}\n"
        f"research_findings: {state.get('research_findings',[])}\n"
        f"memory_context: {state.get('memory_context','')}\n"
        f"authoritative_for_numbers: {settings.AUTHORITATIVE_FOR_NUMBERS}\n"
        f"raw_body:\n{state.get('raw_body','')[:settings.MAX_BODY_TOKENS*4]}\n"
    )
    out = _llm.parse_json(_llm.call_model(system, user, model, max_tokens=3000))
    out["fact_check_model_used"] = model
    out["routing_path"] = _llm.append_route(state, "fact_check")
    out["pipeline_stage"] = "fact_check"
    return out