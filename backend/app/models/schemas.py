"""Pydantic Models & Schemas for Parallax Forensic Engine."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SystemStatus(BaseModel):
    version: str = "1.0.0"
    app_name: str = "Parallax"
    sqlite_wal: str
    ffmpeg_available: bool
    ffmpeg_path: str
    storage_path: str
    is_frozen: bool
    counts: Dict[str, int] = Field(default_factory=dict)


class MediaAssetResponse(BaseModel):
    id: str
    filename: str
    file_type: str
    file_path: str
    file_size_bytes: int
    duration_sec: Optional[float] = None
    page_count: Optional[int] = None
    sha256_hash: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: str


class ClaimResponse(BaseModel):
    id: str
    media_id: str
    speaker: str
    statement: str
    transaction_time_start: float
    transaction_time_end: float
    valid_time_start: Optional[str] = None
    valid_time_end: Optional[str] = None
    confidence: float
    created_at: str


class EvidenceNodeResponse(BaseModel):
    id: str
    media_id: str
    evidence_type: str
    page_number: Optional[int] = None
    bounding_box: Optional[List[float]] = None  # [x1, y1, x2, y2]
    timecode_sec: Optional[float] = None
    extracted_text: str
    valid_time: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: str


class ContradictionResponse(BaseModel):
    id: str
    claim_id: str
    evidence_id: str
    nli_score: float
    nli_label: str
    contradiction_prob: float
    entailment_prob: float
    neutral_prob: float
    reasoning: str
    severity: str
    status: str
    detected_at: str
    # Joined metadata for instant UI rendering
    claim_statement: Optional[str] = None
    claim_speaker: Optional[str] = None
    transaction_time_start: Optional[float] = None
    transaction_time_end: Optional[float] = None
    valid_time: Optional[str] = None
    evidence_text: Optional[str] = None
    evidence_type: Optional[str] = None
    evidence_page: Optional[int] = None
    evidence_box: Optional[List[float]] = None


class BiTemporalPoint(BaseModel):
    id: str
    type: str  # 'claim' | 'evidence' | 'contradiction'
    label: str
    transaction_time_sec: float
    valid_time_iso: str
    score: Optional[float] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BiTemporalHypergraphResponse(BaseModel):
    points: List[BiTemporalPoint]
    claims: List[ClaimResponse]
    evidence_nodes: List[EvidenceNodeResponse]
    contradictions: List[ContradictionResponse]
    summary: Dict[str, Any]


class ExposeCompileRequest(BaseModel):
    contradiction_ids: Optional[List[str]] = None
    fps: int = 60
    resolution: str = "1920x1080"
    split_screen_layout: str = "side_by_side"  # side_by_side | picture_in_picture


class ExposeCompileResponse(BaseModel):
    success: bool
    export_id: str
    output_path: str
    file_size_bytes: int
    duration_sec: float
    fps: int
    contradictions_rendered: int
    ffmpeg_command: str
