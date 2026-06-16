"""LangGraph wiring for the Acton Finance Agent pipeline.

v1 RECONSTRUCTION of the build loop described in the spec doc. The node order and
conditional edges below follow the doc's "Trigger / Gate" table and per-agent
trigger notes, but the exact edge logic is inferred — review against the design
session before relying on it.

Flow:
  memory_start -> [entry: email_monitor | committee_reporter] -> supervisor
  -> deadline_sentinel
  -> (noise? -> memory_end)
  -> analyst (standard|complex by complexity_flag)
  -> (research_flags? -> researcher)
  -> fact_check
  -> narrative_tracker
  -> savings_agent (passive)
  -> (fact_check_passed? -> storyteller)
  -> memory_end
"""

from langgraph.graph import StateGraph, START, END
from state.schema import PipelineState

from agents import (
    supervisor, email_monitor, committee_reporter, analyst, researcher,
    fact_check, storyteller, deadline_sentinel, narrative_tracker,
    savings_agent, memory_agent, scenario_modeler,
)


def _after_supervisor(state: PipelineState) -> str:
    if state.get("document_type") == "noise" or state.get("gate_type") == "no_gate":
        return "memory_end"
    return "deadline_sentinel"


def _needs_research(state: PipelineState) -> str:
    return "researcher" if state.get("research_flags") else "fact_check"


def _after_fact_check(state: PipelineState) -> str:
    return "storyteller" if state.get("fact_check_passed") else "memory_end"


def build_graph(entry: str = "email_monitor"):
    """entry: 'email_monitor' or 'committee_reporter' depending on trigger."""
    g = StateGraph(PipelineState)

    g.add_node("memory_start", memory_agent.memory_start_node)
    g.add_node("email_monitor", email_monitor.email_monitor_node)
    g.add_node("committee_reporter", committee_reporter.committee_reporter_node)
    g.add_node("supervisor", supervisor.supervisor_node)
    g.add_node("deadline_sentinel", deadline_sentinel.deadline_sentinel_node)
    g.add_node("analyst", analyst.analyst_node)            # picks model by complexity_flag
    g.add_node("researcher", researcher.researcher_node)
    g.add_node("fact_check", fact_check.fact_check_node)
    g.add_node("narrative_tracker", narrative_tracker.narrative_tracker_node)
    g.add_node("savings_agent", savings_agent.savings_passive_node)
    g.add_node("storyteller", storyteller.storyteller_node)
    g.add_node("memory_end", memory_agent.memory_end_node)

    g.add_edge(START, "memory_start")
    g.add_edge("memory_start", entry)
    g.add_edge(entry, "supervisor")
    g.add_conditional_edges("supervisor", _after_supervisor,
                            {"deadline_sentinel": "deadline_sentinel", "memory_end": "memory_end"})
    g.add_edge("deadline_sentinel", "analyst")
    g.add_conditional_edges("analyst", _needs_research,
                            {"researcher": "researcher", "fact_check": "fact_check"})
    g.add_edge("researcher", "fact_check")
    g.add_edge("fact_check", "narrative_tracker")
    g.add_edge("narrative_tracker", "savings_agent")
    g.add_conditional_edges("savings_agent", _after_fact_check,
                            {"storyteller": "storyteller", "memory_end": "memory_end"})
    g.add_edge("storyteller", "memory_end")
    g.add_edge("memory_end", END)

    return g.compile()