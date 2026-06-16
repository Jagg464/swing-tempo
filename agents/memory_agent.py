"""Agent 12 — Memory Agent. Shared service: retrieve context (run start), batch write (run end).
Model: Sonnet. Backed by Supabase."""
from config import settings
from agents import _llm
from memory import supabase_client


def memory_start_node(state: dict) -> dict:
    if state.get("dry_run"):
        return {"memory_context": "[dry-run] no prior context.",
                "memory_sources_retrieved": [],
                "routing_path": _llm.append_route(state, "memory_agent_start"),
                "pipeline_stage": "memory_agent_start"}
    # [TODO] supabase_client.retrieve(...) honoring recency, content-type hierarchy, supersession, limit.
    docs = supabase_client.retrieve(state, limit=settings.MEMORY_RETRIEVAL_LIMIT,
                                    months=settings.MEMORY_RECENCY_MONTHS)
    system = _llm.load_prompt("memory_agent")
    context = _llm.call_model(system, f"retrieved:\n{docs}", settings.MODEL_SONNET, max_tokens=1200)
    return {"memory_context": context[: settings.MEMORY_CONTEXT_MAX_WORDS * 8],
            "memory_sources_retrieved": [d.get("id") for d in docs],
            "routing_path": _llm.append_route(state, "memory_agent_start"),
            "pipeline_stage": "memory_agent_start"}


def memory_end_node(state: dict) -> dict:
    if state.get("dry_run"):
        return {"memory_writes_executed": 0, "memory_writes_failed": 0, "memory_write_errors": [],
                "routing_path": _llm.append_route(state, "memory_agent_end"),
                "pipeline_stage": "complete"}
    # [TODO] validate content_type permissions, mark supersession, single batch transaction.
    res = supabase_client.batch_write(state.get("memory_writes", []))
    return {"memory_writes_executed": res.get("ok", 0),
            "memory_writes_failed": res.get("fail", 0),
            "memory_write_errors": res.get("errors", []),
            "routing_path": _llm.append_route(state, "memory_agent_end"),
            "pipeline_stage": "complete"}