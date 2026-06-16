"""Shared helpers: load a prompt file, call the Anthropic Messages API, parse JSON.

In DRY_RUN, callers should short-circuit with mock data rather than hitting the API.
"""

import json
import os
from pathlib import Path
from config import settings

_PROMPT_DIR = Path(__file__).resolve().parent.parent / "prompts"


def load_prompt(name: str) -> str:
    """name without extension, e.g. 'supervisor' -> prompts/supervisor.txt"""
    return (_PROMPT_DIR / f"{name}.txt").read_text(encoding="utf-8")


def call_model(system_prompt: str, user_content: str, model: str, max_tokens: int = 2000) -> str:
    """Single-shot Messages API call. Imported lazily so the repo loads without the SDK."""
    from anthropic import Anthropic
    client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    resp = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_content}],
    )
    return "".join(block.text for block in resp.content if getattr(block, "type", "") == "text")


def parse_json(text: str) -> dict:
    """Parse a model response that should be a single JSON object.
    Strips markdown fences if present. Raises on invalid JSON (fail loud)."""
    t = text.strip()
    if t.startswith("```"):
        t = t.split("```", 2)[1]
        if t.lstrip().startswith("json"):
            t = t.lstrip()[4:]
    return json.loads(t.strip())


def append_route(state: dict, stage: str) -> list:
    return [*state.get("routing_path", []), stage]