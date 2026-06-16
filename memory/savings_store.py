"""Savings project store (stub): gap figures, scored candidates, probability overrides.
Live: persist to Supabase or a local store; snapshot() feeds the pipeline state."""

_STATE = {
    "municipal_gap_dollars": None,
    "school_gap_dollars": None,
    "combined_gap_dollars": None,
    "residual_gap_dollars": None,
    "top_candidates": [],          # filled by Savings Agent scoring
    "savings_last_updated": None,
    "last_checkin_at": None,
    "pending_override_reviews": [],
}


def snapshot() -> dict:
    return dict(_STATE)


def apply(update: dict) -> None:
    for k in _STATE:
        if k in update:
            _STATE[k] = update[k]