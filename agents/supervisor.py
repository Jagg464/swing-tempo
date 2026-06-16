"""Agent 1 — Supervisor. Classifies + routes every run. Model: Haiku."""
from config import settings
from agents import _llm


def supervisor_node(state: dict) -> dict:
    if state.get("dry_run"):
        # mock classification so the graph runs end-to-end
        return {
            "document_type": "budget_material",
            "budget_thread": "thread_b",
            "relevance_score": 0.85,
            "complexity_flag": True,
            "gate_type": "per_item",
            "classification_reasoning": "[dry-run] mock thread_b budget material",
            "routing_path": _llm.append_route(state, "supervisor"),
            "pipeline_stage": "supervisor",
        }
    system = _llm.load_prompt("supervisor")
    user = _build_user(state)
    out = _llm.parse_json(_llm.call_model(system, user, settings.MODEL_HAIKU))
    out["routing_path"] = _llm.append_route(state, "supervisor")
    out["pipeline_stage"] = "supervisor"
    return out


def _build_user(state: dict) -> str:
    return (
        f"raw_sender: {state.get('raw_sender','')}\n"
        f"raw_subject: {state.get('raw_subject','')}\n"
        f"raw_body: {state.get('raw_body','')[:settings.MAX_BODY_TOKENS]}\n"
        f"raw_url: {state.get('raw_url','')}\n"
        f"memory_context: {state.get('memory_context','')}\n"
        f"active_deadlines: {state.get('active_deadlines',[])}\n"
    )