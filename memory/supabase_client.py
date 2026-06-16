"""Supabase memory store (stub). Retrieval honors recency, content-type hierarchy,
supersession, and a 5-doc limit; writes are a single batch transaction at run end."""
from config import settings


def retrieve(state: dict, limit: int = 5, months: int = 6) -> list[dict]:
    if settings.DRY_RUN:
        return []
    raise NotImplementedError("Implement Supabase retrieval with filters.")


def batch_write(writes: list[dict]) -> dict:
    if settings.DRY_RUN:
        return {"ok": 0, "fail": 0, "errors": []}
    raise NotImplementedError("Implement Supabase batch write with supersession + content-type validation.")