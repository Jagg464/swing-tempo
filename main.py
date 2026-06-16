"""Run a single pipeline pass. Entry point for manual / email-triggered runs.

  python main.py                 # dry-run on mock email
  python main.py --reporter      # dry-run on mock agenda (Committee Reporter entry)

Live runs require the REQUIRED items in REQUIRED-BEFORE-DEPLOY.md and DRY_RUN=False.
"""

import argparse
from config import settings
from state.schema import new_state
from graph import build_graph


def run(entry: str = "email_monitor", dry_run: bool = True):
    app = build_graph(entry=entry)
    state = new_state(dry_run=dry_run, trigger_type="email" if entry == "email_monitor" else "scheduled_poll")
    result = app.invoke(state)
    print("pipeline_stage:", result.get("pipeline_stage"))
    print("routing_path:", " -> ".join(result.get("routing_path", [])))
    print("document_type:", result.get("document_type"), "| score:", result.get("relevance_score"))
    if result.get("draft_fincom_memo"):
        print("\n--- FinCom memo (draft) ---\n", result["draft_fincom_memo"][:1200])
    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--reporter", action="store_true", help="use Committee Reporter as entry")
    args = p.parse_args()
    run(entry="committee_reporter" if args.reporter else "email_monitor", dry_run=settings.DRY_RUN)