"""Agents 7 & 8 — Storyteller (FinCom memo + Town post). Model: Sonnet.
Only drafts when fact_check_passed. Writes Word/Excel via tools at the file-writer step."""
from config import settings
from agents import _llm


def storyteller_node(state: dict) -> dict:
    if not state.get("fact_check_passed"):
        return {"routing_path": _llm.append_route(state, "storyteller_skipped"),
                "pipeline_stage": "storyteller"}
    if state.get("dry_run"):
        return {
            "draft_fincom_memo": "[dry-run] DATE: ...\nTO: Acton Finance Committee\nFROM: [Fred — SF.2.1]\nRE: MIIA premium increase\n\nSummary: ...",
            "draft_town_post": "",
            "output_register": "fincom",
            "routing_path": _llm.append_route(state, "storyteller"),
            "pipeline_stage": "storyteller",
        }
    out = {"routing_path": _llm.append_route(state, "storyteller"), "pipeline_stage": "storyteller"}

    # FinCom memo (per_item or digest)
    if state.get("gate_type") in ("per_item", "digest"):
        sys_f = _llm.load_prompt("storyteller_fincom")
        out["draft_fincom_memo"] = _llm.call_model(sys_f, _ctx(state), settings.MODEL_SONNET, max_tokens=3000)
        out["output_register"] = "fincom"
        # [TODO] tools.docx_writer.write_memo(out["draft_fincom_memo"]) -> OUTPUT_ROOT; record output_file_paths

    # Town post only for per_item with public-facing content warranted (human-gated)
    if state.get("gate_type") == "per_item":
        sys_t = _llm.load_prompt("storyteller_town")
        out["draft_town_post"] = _llm.call_model(sys_t, _ctx(state), settings.MODEL_SONNET, max_tokens=1200)
    return out


def _ctx(state: dict) -> str:
    return (
        f"document_type: {state.get('document_type')}\n"
        f"raw_subject: {state.get('raw_subject','')}\n"
        f"extracted_numbers: {state.get('extracted_numbers',{})}\n"
        f"budget_impact_summary: {state.get('budget_impact_summary','')}\n"
        f"variance_from_forecast: {state.get('variance_from_forecast',{})}\n"
        f"analyst_flags: {state.get('analyst_flags',[])}\n"
        f"research_flags: {state.get('research_flags',[])}\n"
        f"residual_gap_dollars: {state.get('residual_gap_dollars')}\n"
        f"combined_gap_dollars: {state.get('combined_gap_dollars')}\n"
        f"top_candidates: {state.get('top_candidates',[])}\n"
        f"memory_context: {state.get('memory_context','')}\n"
        f"household_count: {settings.ACTON_HOUSEHOLD_COUNT}\n"
    )