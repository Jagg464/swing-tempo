"""Agent 5 — Researcher. Resolves research_flags + proactive context. Model: Sonnet."""
from config import settings
from agents import _llm


def researcher_node(state: dict) -> dict:
    if state.get("dry_run"):
        return {
            "research_findings": [],
            "sources_consulted": [],
            "routing_path": _llm.append_route(state, "researcher"),
            "pipeline_stage": "researcher",
        }
    system = _llm.load_prompt("researcher")
    user = (
        f"research_flags: {state.get('research_flags',[])}\n"
        f"relevance_score: {state.get('relevance_score')}\n"
        f"peer_municipalities: {settings.PEER_MUNICIPALITIES}\n"
        f"proactive_max_sources: {settings.PROACTIVE_RESEARCH_MAX_SOURCES}\n"
    )
    # [TODO] give the Researcher web access (httpx/Playwright via tools.web_fetch) within source hierarchy.
    out = _llm.parse_json(_llm.call_model(system, user, settings.MODEL_SONNET, max_tokens=3000))
    out["routing_path"] = _llm.append_route(state, "researcher")
    out["pipeline_stage"] = "researcher"
    return out