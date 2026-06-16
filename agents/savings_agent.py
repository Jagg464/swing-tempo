"""Agent 11 — Savings Agent. Maintains the 2.5%-target gap + candidate scoring. Model: Opus.
Passive (every budget run) + Active (first Sunday monthly check-in email)."""
from config import settings
from agents import _llm
from memory import savings_store


def savings_passive_node(state: dict) -> dict:
    if state.get("dry_run"):
        snap = savings_store.snapshot()
        snap["routing_path"] = _llm.append_route(state, "savings_agent")
        snap["pipeline_stage"] = "savings_agent"
        return snap
    system = _llm.load_prompt("savings_agent")
    user = (
        f"mode: passive\n"
        f"extracted_numbers: {state.get('extracted_numbers',{})}\n"
        f"budget_thread: {state.get('budget_thread')}\n"
        f"alg_assumptions: {settings.ALG_ASSUMPTIONS}\n"
        f"store: {savings_store.snapshot()}\n"
    )
    out = _llm.parse_json(_llm.call_model(system, user, settings.MODEL_OPUS, max_tokens=3000))
    savings_store.apply(out)   # persist gap/candidate updates
    out["routing_path"] = _llm.append_route(state, "savings_agent")
    out["pipeline_stage"] = "savings_agent"
    return out


def savings_monthly_checkin():
    """Active mode — first Sunday. Emails Fred the check-in, parses his reply.
    [TODO] wire tools.gmail_client send + reply parsing into savings_store overrides."""
    raise NotImplementedError("Wire monthly check-in (email send + reply parse).")