"""Agent 3 — Committee Reporter. Monitors public sites nightly, fills Group 1. Model: Haiku."""
from pathlib import Path
from config import settings
from agents import _llm

_MOCK = Path(__file__).resolve().parent.parent / "tests" / "mock_data" / "sample_agenda.html"


def committee_reporter_node(state: dict) -> dict:
    if state.get("dry_run"):
        return {
            "raw_sender": "Acton Finance Committee",
            "raw_subject": "FinCom Meeting Agenda — [dry-run mock]",
            "raw_body": _MOCK.read_text()[: settings.MAX_BODY_TOKENS * 4],
            "raw_url": "https://www.acton-ma.gov/mock-agenda",
            "trigger_type": "scheduled_poll",
            "source": "acton-ma.gov",
            "received_at": "",
            "routing_path": _llm.append_route(state, "committee_reporter"),
            "pipeline_stage": "committee_reporter",
        }
    # [TODO] tools.web_fetch: for each MONITORED_SITES entry, fetch (httpx/Playwright),
    #        diff against memory last_seen_content, emit one run per NEW document.
    raise NotImplementedError("Wire tools.web_fetch + MONITORED_SITES for live monitoring.")