"""Forensic Fixture Generator for Parallax.

Seeds the SQLite database with a realistic, high-stakes corporate fraud &
deposition hearing dataset: "SEC vs. Apex Global Logistics (2023-2024)".
Provides rich multi-modal claims, PDF bounding box coordinates, and DeBERTa NLI scores.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from backend.app.db.database import get_db, init_db

FIXTURE_ASSETS = [
    {
        "id": "asset_video_01",
        "filename": "apex_ceo_q3_deposition.mp4",
        "file_type": "video",
        "file_path": "raw/apex_ceo_q3_deposition.mp4",
        "file_size_bytes": 148_290_120,
        "duration_sec": 724.50,
        "page_count": None,
        "sha256_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "metadata": {
            "title": "Deposition of CEO Marcus Vance (Case No. 23-CV-8819)",
            "codec": "h264",
            "fps": 60,
            "resolution": "1920x1080",
            "recorded_at": "2024-02-14T10:00:00Z"
        }
    },
    {
        "id": "asset_pdf_01",
        "filename": "exhibit_c_audited_escrow_ledger.pdf",
        "file_type": "pdf",
        "file_path": "raw/exhibit_c_audited_escrow_ledger.pdf",
        "file_size_bytes": 4_210_880,
        "duration_sec": None,
        "page_count": 38,
        "sha256_hash": "8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4",
        "metadata": {
            "title": "Deloitte & Touche Q3 Forensic Escrow & Lien Audit",
            "submitted_by": "Special Counsel",
            "signed_date": "2023-09-30"
        }
    },
    {
        "id": "asset_pdf_02",
        "filename": "exhibit_f_internal_wire_authorization.pdf",
        "file_type": "pdf",
        "file_path": "raw/exhibit_f_internal_wire_authorization.pdf",
        "file_size_bytes": 1_820_140,
        "duration_sec": None,
        "page_count": 12,
        "sha256_hash": "a1b2c3d4e5f60718293a4b5c6d7e8f90123456789abcdef0123456789abcdef0",
        "metadata": {
            "title": "Apex Treasury Internal Swift Wire Confirmation ($14.2M Cayman)",
            "classification": "CONFIDENTIAL",
            "timestamp": "2023-06-18T16:22:00Z"
        }
    }
]

FIXTURE_CLAIMS = [
    {
        "id": "claim_01",
        "media_id": "asset_video_01",
        "speaker": "Marcus Vance (CEO)",
        "statement": "At no point prior to September 15, 2023, did Apex Global transfer any corporate capital to offshore Cayman subsidiaries or Cayman accounts.",
        "transaction_time_start": 84.20,
        "transaction_time_end": 96.80,
        "valid_time_start": "2023-01-01T00:00:00Z",
        "valid_time_end": "2023-09-15T00:00:00Z",
        "confidence": 0.99
    },
    {
        "id": "claim_02",
        "media_id": "asset_video_01",
        "speaker": "Marcus Vance (CEO)",
        "statement": "Our total unencumbered liquidity at the close of Q2 was well above forty million dollars, with zero outstanding third-party liens.",
        "transaction_time_start": 218.40,
        "transaction_time_end": 231.10,
        "valid_time_start": "2023-06-30T00:00:00Z",
        "valid_time_end": "2023-06-30T23:59:59Z",
        "confidence": 0.97
    },
    {
        "id": "claim_03",
        "media_id": "asset_video_01",
        "speaker": "Marcus Vance (CEO)",
        "statement": "The maritime fleet lease agreement was renewed on standard terms in July, without granting any senior collateral pledges to lenders.",
        "transaction_time_start": 412.50,
        "transaction_time_end": 427.00,
        "valid_time_start": "2023-07-01T00:00:00Z",
        "valid_time_end": "2023-07-31T23:59:59Z",
        "confidence": 0.96
    },
    {
        "id": "claim_04",
        "media_id": "asset_video_01",
        "speaker": "Marcus Vance (CEO)",
        "statement": "We notified the Board of Directors immediately within 24 hours of receiving the European Maritime Safety Agency notice on August 12.",
        "transaction_time_start": 580.00,
        "transaction_time_end": 593.40,
        "valid_time_start": "2023-08-12T00:00:00Z",
        "valid_time_end": "2023-08-13T23:59:59Z",
        "confidence": 0.98
    }
]

FIXTURE_EVIDENCE = [
    {
        "id": "evidence_01",
        "media_id": "asset_pdf_02",
        "evidence_type": "pdf_clause",
        "page_number": 4,
        "bounding_box": [0.12, 0.48, 0.88, 0.62],
        "timecode_sec": None,
        "extracted_text": "SWIFT MT103 REF #KY7781-B: Outbound Wire USD 14,200,000.00 from Apex Ops Acct 8821 to Apex Cayman Holdings Ltd (Bank of Nova Scotia, George Town, KY). Auth: M. Vance.",
        "valid_time": "2023-06-18T16:22:00Z",
        "metadata": {"doc_section": "Item 4.2 - Non-Operating Wire Transfers", "signatory": "Marcus Vance"}
    },
    {
        "id": "evidence_02",
        "media_id": "asset_pdf_01",
        "evidence_type": "pdf_clause",
        "page_number": 19,
        "bounding_box": [0.10, 0.28, 0.90, 0.44],
        "timecode_sec": None,
        "extracted_text": "NOTE 8 (SENIOR SECURED LIENS): As of June 30, 2023, available liquidity was constrained by a $28.5M senior perfection lien held by Fortress Maritime Credit Partners LP.",
        "valid_time": "2023-06-30T00:00:00Z",
        "metadata": {"doc_section": "Footnote 8: Contingent Liens", "auditor": "Deloitte"}
    },
    {
        "id": "evidence_03",
        "media_id": "asset_pdf_01",
        "evidence_type": "pdf_clause",
        "page_number": 27,
        "bounding_box": [0.14, 0.70, 0.86, 0.86],
        "timecode_sec": None,
        "extracted_text": "Section 9.1: In consideration for lease extension, Apex assigns a first-priority security interest in all hulls, freight receivables, and salvage rights to Vessel Lessor LLC.",
        "valid_time": "2023-07-15T00:00:00Z",
        "metadata": {"doc_section": "Master Maritime Lease Amendment", "collateral": "First-Priority Senior"}
    },
    {
        "id": "evidence_04",
        "media_id": "asset_pdf_01",
        "evidence_type": "pdf_clause",
        "page_number": 34,
        "bounding_box": [0.15, 0.52, 0.85, 0.65],
        "timecode_sec": None,
        "extracted_text": "Board Minute Excerpt: The Chair presented EMSA sanction findings to the Board for the first time during the September 28 Quarterly Meeting, 47 days after notice receipt.",
        "valid_time": "2023-09-28T14:00:00Z",
        "metadata": {"doc_section": "Apex Board Minutes", "delay_days": 47}
    }
]

FIXTURE_CONTRADICTIONS = [
    {
        "id": "contra_01",
        "claim_id": "claim_01",
        "evidence_id": "evidence_01",
        "nli_score": 0.962,
        "nli_label": "CONTRADICTION",
        "contradiction_prob": 0.962,
        "entailment_prob": 0.015,
        "neutral_prob": 0.023,
        "reasoning": "CEO explicitly testified under oath that no capital was transferred to Cayman entities before Sept 15, 2023. Wire Ref #KY7781-B proves a $14,200,000.00 outbound transfer to George Town, KY authorized by Vance on June 18, 2023.",
        "severity": "CRITICAL",
        "status": "VERIFIED"
    },
    {
        "id": "contra_02",
        "claim_id": "claim_02",
        "evidence_id": "evidence_02",
        "nli_score": 0.938,
        "nli_label": "CONTRADICTION",
        "contradiction_prob": 0.938,
        "entailment_prob": 0.024,
        "neutral_prob": 0.038,
        "reasoning": "CEO claimed over $40M in unencumbered liquidity with 'zero outstanding liens'. Audited Note 8 confirms $28.5M was encumbered under an active senior perfection lien by Fortress Maritime.",
        "severity": "CRITICAL",
        "status": "VERIFIED"
    },
    {
        "id": "contra_03",
        "claim_id": "claim_03",
        "evidence_id": "evidence_03",
        "nli_score": 0.894,
        "nli_label": "CONTRADICTION",
        "contradiction_prob": 0.894,
        "entailment_prob": 0.042,
        "neutral_prob": 0.064,
        "reasoning": "CEO denied granting any senior collateral pledges during the July fleet renewal. Section 9.1 explicitly assigns a first-priority security interest in all hulls and freight receivables.",
        "severity": "HIGH",
        "status": "DETECTED"
    },
    {
        "id": "contra_04",
        "claim_id": "claim_04",
        "evidence_id": "evidence_04",
        "nli_score": 0.915,
        "nli_label": "CONTRADICTION",
        "contradiction_prob": 0.915,
        "entailment_prob": 0.031,
        "neutral_prob": 0.054,
        "reasoning": "CEO claimed Board was alerted 'within 24 hours' of August 12. Corporate board minutes prove disclosure did not occur until September 28, representing a 47-day material concealment.",
        "severity": "HIGH",
        "status": "DETECTED"
    }
]


def seed_fixtures(db_path: Path | None = None) -> Dict[str, Any]:
    """Seed the SQLite database with the forensic investigation dataset."""
    init_db(db_path=db_path)
    with get_db(db_path=db_path) as conn:
        # Clear existing
        conn.execute("DELETE FROM contradictions;")
        conn.execute("DELETE FROM evidence_nodes;")
        conn.execute("DELETE FROM claims;")
        conn.execute("DELETE FROM media_assets;")

        # Insert Assets
        for asset in FIXTURE_ASSETS:
            conn.execute(
                """
                INSERT INTO media_assets (id, filename, file_type, file_path, file_size_bytes, duration_sec, page_count, sha256_hash, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    asset["id"],
                    asset["filename"],
                    asset["file_type"],
                    asset["file_path"],
                    asset["file_size_bytes"],
                    asset["duration_sec"],
                    asset["page_count"],
                    asset["sha256_hash"],
                    json.dumps(asset["metadata"])
                )
            )

        # Insert Claims
        for claim in FIXTURE_CLAIMS:
            conn.execute(
                """
                INSERT INTO claims (id, media_id, speaker, statement, transaction_time_start, transaction_time_end, valid_time_start, valid_time_end, confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    claim["id"],
                    claim["media_id"],
                    claim["speaker"],
                    claim["statement"],
                    claim["transaction_time_start"],
                    claim["transaction_time_end"],
                    claim["valid_time_start"],
                    claim["valid_time_end"],
                    claim["confidence"]
                )
            )

        # Insert Evidence Nodes
        for ev in FIXTURE_EVIDENCE:
            conn.execute(
                """
                INSERT INTO evidence_nodes (id, media_id, evidence_type, page_number, bounding_box, timecode_sec, extracted_text, valid_time, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    ev["id"],
                    ev["media_id"],
                    ev["evidence_type"],
                    ev["page_number"],
                    json.dumps(ev["bounding_box"]) if ev["bounding_box"] else None,
                    ev["timecode_sec"],
                    ev["extracted_text"],
                    ev["valid_time"],
                    json.dumps(ev["metadata"])
                )
            )

        # Insert Contradictions
        for contra in FIXTURE_CONTRADICTIONS:
            conn.execute(
                """
                INSERT INTO contradictions (id, claim_id, evidence_id, nli_score, nli_label, contradiction_prob, entailment_prob, neutral_prob, reasoning, severity, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    contra["id"],
                    contra["claim_id"],
                    contra["evidence_id"],
                    contra["nli_score"],
                    contra["nli_label"],
                    contra["contradiction_prob"],
                    contra["entailment_prob"],
                    contra["neutral_prob"],
                    contra["reasoning"],
                    contra["severity"],
                    contra["status"]
                )
            )

        conn.commit()

    return {
        "status": "success",
        "assets_seeded": len(FIXTURE_ASSETS),
        "claims_seeded": len(FIXTURE_CLAIMS),
        "evidence_seeded": len(FIXTURE_EVIDENCE),
        "contradictions_seeded": len(FIXTURE_CONTRADICTIONS)
    }
