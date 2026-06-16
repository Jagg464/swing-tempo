"""Central configuration. Most tuning lives here so behavior changes need no code edits.
Items tagged with a review-question ID (e.g. G.1, SUP.1.1) are tracked in
REQUIRED-BEFORE-DEPLOY.md."""

import os
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# MODELS
# NOTE: the spec doc said Opus "claude-opus-4-7"; the current Opus is
# "claude-opus-4-8". Set to 4-8 here — confirm the exact slug against the
# Anthropic model list before live use, then leave it.
# ---------------------------------------------------------------------------
MODEL_HAIKU  = "claude-haiku-4-5-20251001"
MODEL_SONNET = "claude-sonnet-4-6"
MODEL_OPUS   = "claude-opus-4-8"   # doc said 4-7 — confirm (see flag)

# ---------------------------------------------------------------------------
# SECRETS / PATHS (from .env)
# ---------------------------------------------------------------------------
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
SUPABASE_URL      = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY      = os.getenv("SUPABASE_KEY", "")
OUTPUT_ROOT       = os.getenv("OUTPUT_ROOT", "")          # G.1 REQUIRED
AGENT_GMAIL       = os.getenv("AGENT_GMAIL_ADDRESS", "")  # G.3 REQUIRED
FRED_NOTIFY_GMAIL = os.getenv("FRED_NOTIFY_GMAIL", "")    # G.2 REQUIRED

# ---------------------------------------------------------------------------
# SUPERVISOR / ROUTING THRESHOLDS
# ---------------------------------------------------------------------------
PER_ITEM_THRESHOLD = 0.80   # G.6 — revisit after 2 weeks live
DIGEST_FLOOR       = 0.40   # G.6
MAX_BODY_TOKENS    = 8000   # G.4
COMPLEXITY_TOKEN_THRESHOLD = 4000   # G.5

# ---------------------------------------------------------------------------
# EMAIL MONITOR
# ---------------------------------------------------------------------------
# EM.3.1 / Agent 2 Section 3 — extend as you see real inbox traffic
EMAIL_SKIP_DOMAINS = [
    # "examplemarketing.com",
]
# EM.4.1 / Agent 2 Section 4 — formal sender name mappings
EMAIL_SENDER_MAP = {
    "town-manager@acton-ma.gov": "Town Manager",
    "selectboard@acton-ma.gov":  "Acton Select Board",
    "fincom@acton-ma.gov":       "Acton Finance Committee",
}
GMAIL_POLL_SECONDS = 900   # CR.2.3 / EM — polling cadence

# ---------------------------------------------------------------------------
# COMMITTEE REPORTER (web monitoring)
# CR.2.1 / SUP — confirm URLs before live use (PLACEHOLDER)
# ---------------------------------------------------------------------------
MONITORED_SITES = [
    # {"name": "Acton Select Board", "url": "https://www.acton-ma.gov/...", "render": "httpx", "sender": "Acton Select Board"},
    # {"name": "Acton Finance Committee", "url": "https://www.acton-ma.gov/...", "render": "httpx", "sender": "Acton Finance Committee"},
    # {"name": "ABRSD AgendaCenter", "url": "https://www.boxborough-ma.gov/AgendaCenter", "render": "playwright", "sender": "AB School Committee"},
    # {"name": "Acton Beacon", "url": "https://CONFIRM-URL", "render": "httpx", "sender": "Acton Beacon"},   # CR.2.1 / G.8
]
SITE_SENDER_MAP = {
    # "acton-ma.gov": "Town of Acton",
    # "boxborough-ma.gov": "AB School Committee",
}
FETCH_MIN_INTERVAL_SECONDS = 2     # politeness: per-domain
RETRY_DELAY_SECONDS = 30

# ---------------------------------------------------------------------------
# ANALYST — ALG MODEL ASSUMPTIONS (AN.2.1 REQUIRED — populate ~June 2026)
# ---------------------------------------------------------------------------
ALG_ASSUMPTIONS = {
    "municipal_growth_target_pct": 2.5,
    "school_growth_target_pct": 2.5,
    "structural_gap": None,                      # AN.2.1 TO BE CONFIRMED
    "health_insurance_trend_pct": None,          # from MIIA
    "state_aid_growth_pct": None,                # from Cherry Sheet
    "new_growth_assumption": None,               # from Assessors
    "prior_year_municipal_operating_budget": None,  # AN.2.2 / SA.2.1 REQUIRED
    "prior_year_abrsd_assessment_acton_share": None, # AN.2.3 / SA.2.2 REQUIRED
    "municipal_operating_budget_total": None,    # AN.2.2 REQUIRED (% calcs)
}

# ---------------------------------------------------------------------------
# RESEARCHER (RE.3.1 REQUIRED — peer towns)
# ---------------------------------------------------------------------------
PEER_MUNICIPALITIES = [
    # "Westford", "Bedford", "...",  # RE.3.1 — comparable by size/tax base/regional school
]
PROACTIVE_RESEARCH_MAX_SOURCES = 3   # RE.4.1

# ---------------------------------------------------------------------------
# DEADLINE SENTINEL — budget calendar (DS.2.1 / DS.2.2 REQUIRED — confirm dates)
# Each gate: name, iso_date (fill), alert_threshold_days, deliverable
# ---------------------------------------------------------------------------
BUDGET_GATES = [
    {"gate": "Select Board Budget Guidance",  "date": None, "threshold_days": 45, "deliverable": "FinCom recommendation on guidance parameters"},
    {"gate": "Department Budget Submissions", "date": None, "threshold_days": 30, "deliverable": "All department requests to Town Manager"},
    {"gate": "Town Manager Budget Proposal",  "date": None, "threshold_days": 21, "deliverable": "Full budget proposal for FinCom review"},
    {"gate": "FinCom Budget Adoption Vote",   "date": None, "threshold_days": 30, "deliverable": "FinCom formal budget adoption"},
    {"gate": "FinCom Recommendation Vote",    "date": None, "threshold_days": 30, "deliverable": "Formal FinCom recommendation to Town Meeting"},
    {"gate": "Warrant Closing",               "date": None, "threshold_days": 21, "deliverable": "All warrant articles finalized"},
    {"gate": "Annual Town Meeting (ATM)",     "date": None, "threshold_days": 45, "deliverable": "FinCom presentation and floor support"},
    # DS.2.2 — add ABRSD budget cycle gates (school assessment timeline differs)
]
SAVINGS_STALENESS_DAYS = 7
SAVINGS_CHECKIN_OVERDUE_DAYS = 35

# ---------------------------------------------------------------------------
# NARRATIVE TRACKER
# ---------------------------------------------------------------------------
NARRATIVE_WINDOW_DAYS = 30   # NT.4.1

# ---------------------------------------------------------------------------
# MEMORY AGENT
# ---------------------------------------------------------------------------
MEMORY_RECENCY_MONTHS = 6        # MA.2.1
MEMORY_CONTEXT_MAX_WORDS = 500   # MA.2.2
MEMORY_RETRIEVAL_LIMIT = 5

CONTENT_TYPE_PERMISSIONS = {
    "official_budget_document": ["numbers", "narrative", "positions"],
    "capital_plan":             ["numbers", "narrative", "positions"],
    "town_manager_memo":        ["numbers", "narrative", "positions"],
    "meeting_minutes":          ["narrative", "positions"],
    "public_statement":         ["narrative", "positions"],
    "media_coverage":           ["narrative"],
    "research_finding":         ["narrative", "positions"],
}
# Authoritative for number verification (Fact-Check supersession rule)
AUTHORITATIVE_FOR_NUMBERS = ["official_budget_document", "capital_plan", "town_manager_memo"]

# ---------------------------------------------------------------------------
# SAVINGS AGENT
# ---------------------------------------------------------------------------
ACTON_HOUSEHOLD_COUNT = None   # G.7 / SF.4.1 / ST.4.1 REQUIRED
SAVINGS_CHECKIN_WEEKDAY = 6    # SA.5.1 — first Sunday of month (0=Mon..6=Sun)

# ---------------------------------------------------------------------------
# SCENARIO MODELER (stub — not active)
# ---------------------------------------------------------------------------
SCENARIO_MODELER_ACTIVE = False
SCENARIO_TRIGGERS = [
    "union_negotiation_open",
    "initial_budget_submission",
    "abrsd_assessment_proposal",
    "capital_plan_draft_release",
    "state_aid_preliminary_numbers",
]

DRY_RUN = True   # flip to False only after the REQUIRED items are filled