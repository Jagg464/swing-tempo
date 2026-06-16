"""Agent 10 — Narrative Tracker. Pattern detection across public venues. Model: Haiku."""
from config import settings
from agents import _llm


def narrative_tracker_node(state: dict) -> dict:
    if state.get("dry_run"):
        return {"narrative_flags": [],
                "routing_path": _llm.append_route(state, "narrative_tracker"),
                "pipeline_stage": "narrative_tracker"}
    system = _llm.load_prompt("narrative_tracker")
    user = (
        f"raw_sender: {state.get('raw_sender','')}\n"
        f"raw_subject: {state.get('raw_subject','')}\n"
        f"raw_body:\n{state.get('raw_body','')[:settings.MAX_BODY_TOKENS*4]}\n"
        f"window_days: {settings.NARRATIVE_WINDOW_DAYS}\n"
        f"memory_context: {state.get('memory_context','')}\n"
    )
    out = _llm.parse_json(_llm.call_model(system, user, settings.MODEL_HAIKU))
    out["routing_path"] = _llm.append_route(state, "narrative_tracker")
    out["pipeline_stage"] = "narrative_tracker"
    return out