"""Contradiction Analysis & NLI Hunt Router."""

from __future__ import annotations

import json
from typing import List

from fastapi import APIRouter

from backend.app.db.database import get_db
from backend.app.models.schemas import ContradictionResponse
from backend.app.services.nli import NLIHunter

router = APIRouter(prefix="/api/analysis", tags=["Analysis"])


@router.get("/contradictions", response_model=List[ContradictionResponse])
async def list_contradictions() -> List[ContradictionResponse]:
    """List all detected cross-modal contradictions joined with claim and evidence details."""
    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT
                ct.id, ct.claim_id, ct.evidence_id, ct.nli_score, ct.nli_label,
                ct.contradiction_prob, ct.entailment_prob, ct.neutral_prob,
                ct.reasoning, ct.severity, ct.status, ct.detected_at,
                c.statement AS claim_statement, c.speaker AS claim_speaker,
                c.transaction_time_start, c.transaction_time_end,
                e.valid_time, e.extracted_text AS evidence_text,
                e.evidence_type, e.page_number AS evidence_page,
                e.bounding_box AS evidence_box
            FROM contradictions ct
            JOIN claims c ON ct.claim_id = c.id
            JOIN evidence_nodes e ON ct.evidence_id = e.id
            ORDER BY ct.nli_score DESC
            """
        ).fetchall()

        results = []
        for r in rows:
            box = json.loads(r["evidence_box"]) if r["evidence_box"] else None
            results.append(
                ContradictionResponse(
                    id=r["id"],
                    claim_id=r["claim_id"],
                    evidence_id=r["evidence_id"],
                    nli_score=r["nli_score"],
                    nli_label=r["nli_label"],
                    contradiction_prob=r["contradiction_prob"],
                    entailment_prob=r["entailment_prob"],
                    neutral_prob=r["neutral_prob"],
                    reasoning=r["reasoning"],
                    severity=r["severity"],
                    status=r["status"],
                    detected_at=str(r["detected_at"]),
                    claim_statement=r["claim_statement"],
                    claim_speaker=r["claim_speaker"],
                    transaction_time_start=r["transaction_time_start"],
                    transaction_time_end=r["transaction_time_end"],
                    valid_time=r["valid_time"],
                    evidence_text=r["evidence_text"],
                    evidence_type=r["evidence_type"],
                    evidence_page=r["evidence_page"],
                    evidence_box=box,
                )
            )
        return results


@router.post("/hunt")
async def trigger_hunt():
    """Trigger DeBERTa NLI Cross-Encoder Contradiction Hunter across all claims and evidence."""
    return NLIHunter.run_hunt()
