"""Agent 2 — Email Monitor. Retrieves unread mail, pre-filters, fills Group 1. Model: Haiku."""
import json
from pathlib import Path
from config import settings
from agents import _llm

_MOCK = Path(__file__).resolve().parent.parent / "tests" / "mock_data" / "sample_email.json"


def email_monitor_node(state: dict) -> dict:
    if state.get("dry_run"):
        msg = json.loads(_MOCK.read_text())
        return {
            **_extract(msg),
            "routing_path": _llm.append_route(state, "email_monitor"),
            "pipeline_stage": "email_monitor",
        }
    # [TODO] tools.gmail_client: list unread, apply EMAIL_SKIP_DOMAINS/dedupe, per-message run.
    raise NotImplementedError("Wire tools.gmail_client for live email monitoring.")


def _extract(msg: dict) -> dict:
    sender = settings.EMAIL_SENDER_MAP.get(msg.get("from_email", ""), msg.get("from_name") or msg.get("from_email", ""))
    body = msg.get("body", "")
    for att in msg.get("attachments", []):
        if att.get("type") in ("pdf", "xlsx", "docx"):
            body += f"\n[ATTACHMENT DETECTED: {att.get('filename')} — manual review may be needed]"
    return {
        "raw_sender": sender,
        "raw_subject": msg.get("subject") or f"[No Subject] from {sender}",
        "raw_body": body[: settings.MAX_BODY_TOKENS * 4],
        "raw_url": "",
        "trigger_type": "email",
        "source": "gmail",
        "received_at": msg.get("received_at", ""),
        "attachments": msg.get("attachments", []),
    }