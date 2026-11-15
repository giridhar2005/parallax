"""Bi-Temporal Hypergraph Engine.

Constructs 2D temporal topology mapping Transaction Time (media playback seconds)
against Valid Time (historical calendar events referenced).
"""

from __future__ import annotations

import json
from typing import List

from backend.app.db.database import get_db
from backend.app.models.schemas import (
    BiTemporalHypergraphResponse,
    BiTemporalPoint,
    ClaimResponse,
    ContradictionResponse,
    EvidenceNodeResponse,
)


def get_bitemporal_graph() -> BiTemporalHypergraphResponse:
    """Query and assemble full bi-temporal graph nodes and contradiction edges."""
    with get_db() as conn:
        # 1. Claims
        claims_rows = conn.execute(
            """
            SELECT id, media_id, speaker, statement, transaction_time_start,
                   transaction_time_end, valid_time_start, valid_time_end,
                   confidence, created_at
            FROM claims ORDER BY transaction_time_start ASC
            """
        ).fetchall()

        # 2. Evidence
        evidence_rows = conn.execute(
            """
            SELECT id, media_id, evidence_type, page_number, bounding_box,
                   timecode_sec, extracted_text, valid_time, metadata, created_at
            FROM evidence_nodes ORDER BY valid_time ASC
            """
        ).fetchall()

        # 3. Contradictions with joined claim and evidence data
        contradiction_rows = conn.execute(
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

    claims: List[ClaimResponse] = []
    points: List[BiTemporalPoint] = []

    for r in claims_rows:
        cr = ClaimResponse(
            id=r["id"],
            media_id=r["media_id"],
            speaker=r["speaker"],
            statement=r["statement"],
            transaction_time_start=r["transaction_time_start"],
            transaction_time_end=r["transaction_time_end"],
            valid_time_start=r["valid_time_start"],
            valid_time_end=r["valid_time_end"],
            confidence=r["confidence"],
            created_at=str(r["created_at"]),
        )
        claims.append(cr)
        points.append(
            BiTemporalPoint(
                id=cr.id,
                type="claim",
                label=f"{cr.speaker}: {cr.statement[:40]}...",
                transaction_time_sec=cr.transaction_time_start,
                valid_time_iso=cr.valid_time_start or "2023-01-01T00:00:00Z",
                metadata={"speaker": cr.speaker, "confidence": cr.confidence},
            )
        )

    evidence_nodes: List[EvidenceNodeResponse] = []
    for r in evidence_rows:
        box = json.loads(r["bounding_box"]) if r["bounding_box"] else None
        meta = json.loads(r["metadata"]) if r["metadata"] else {}
        ev = EvidenceNodeResponse(
            id=r["id"],
            media_id=r["media_id"],
            evidence_type=r["evidence_type"],
            page_number=r["page_number"],
            bounding_box=box,
            timecode_sec=r["timecode_sec"],
            extracted_text=r["extracted_text"],
            valid_time=r["valid_time"],
            metadata=meta,
            created_at=str(r["created_at"]),
        )
        evidence_nodes.append(ev)

    contradictions: List[ContradictionResponse] = []
    for r in contradiction_rows:
        box = json.loads(r["evidence_box"]) if r["evidence_box"] else None
        contra = ContradictionResponse(
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
        contradictions.append(contra)
        points.append(
            BiTemporalPoint(
                id=contra.id,
                type="contradiction",
                label=f"Contradiction ({contra.nli_score:.2f})",
                transaction_time_sec=contra.transaction_time_start or 0.0,
                valid_time_iso=contra.valid_time or "2023-01-01T00:00:00Z",
                score=contra.nli_score,
                metadata={
                    "severity": contra.severity,
                    "reasoning": contra.reasoning,
                    "claim_id": contra.claim_id,
                    "evidence_id": contra.evidence_id,
                },
            )
        )

    summary = {
        "total_claims": len(claims),
        "total_evidence": len(evidence_nodes),
        "total_contradictions": len(contradictions),
        "critical_count": sum(1 for c in contradictions if c.severity == "CRITICAL"),
        "high_count": sum(1 for c in contradictions if c.severity == "HIGH"),
        "top_nli_score": max((c.nli_score for c in contradictions), default=0.0),
    }

    return BiTemporalHypergraphResponse(
        points=points,
        claims=claims,
        evidence_nodes=evidence_nodes,
        contradictions=contradictions,
        summary=summary,
    )
