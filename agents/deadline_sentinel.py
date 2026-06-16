"""Agent 9 — Deadline Sentinel. Updates active_deadlines, fires alerts, checks scenario triggers.
Model: Haiku."""
from config import settings
from agents import _llm


def deadline_sentinel_node(state: dict) -> dict:
    if state.get("dry_run"):
        return {
            "active_deadlines": [{"gate": g["gate"], "days_remaining": None} for g in settings.BUDGET_GATES],
            "sentinel_notes": [],
            "scenario_modeler_triggered": False,
            "routing_path": _llm.append_route(state, "deadline_sentinel"),
            "pipeline_stage": "deadline_sentinel",
        }
    # [TODO] compute days_remaining from BUDGET_GATES dates; fire alerts at threshold,
    #        threshold/2, 7 days, day-of (dedupe per gate/threshold in memory); check
    #        SCENARIO_TRIGGERS; check savings staleness/checkin overdue.
    system = _llm.load_prompt("deadline_sentinel")
    out = _llm.parse_json(_llm.call_model(system, _user(state), settings.MODEL_HAIKU))
    out["routing_path"] = _llm.append_route(state, "deadline_sentinel")
    out["pipeline_stage"] = "deadline_sentinel"
    return out


def _user(state: dict) -> str:
    return (
        f"budget_gates: {settings.BUDGET_GATES}\n"
        f"savings_last_updated: {state.get('savings_last_updated')}\n"
        f"last_checkin_at: {state.get('last_checkin_at')}\n"
        f"residual_gap_dollars: {state.get('residual_gap_dollars')}\n"
    )