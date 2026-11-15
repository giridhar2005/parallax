"""Media Asset Ingestion & Retrieval Router."""

from __future__ import annotations

import hashlib
import json
import uuid
from typing import List

from fastapi import APIRouter, File, UploadFile

from backend.app.config import settings
from backend.app.db.database import get_db
from backend.app.models.schemas import MediaAssetResponse

router = APIRouter(prefix="/api/media", tags=["Media"])


@router.get("/list", response_model=List[MediaAssetResponse])
async def list_media() -> List[MediaAssetResponse]:
    """List all ingested media files (video recordings and evidentiary PDFs)."""
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM media_assets ORDER BY created_at DESC").fetchall()
        results = []
        for r in rows:
            meta = json.loads(r["metadata"]) if r["metadata"] else {}
            results.append(
                MediaAssetResponse(
                    id=r["id"],
                    filename=r["filename"],
                    file_type=r["file_type"],
                    file_path=r["file_path"],
                    file_size_bytes=r["file_size_bytes"],
                    duration_sec=r["duration_sec"],
                    page_count=r["page_count"],
                    sha256_hash=r["sha256_hash"],
                    metadata=meta,
                    created_at=str(r["created_at"]),
                )
            )
        return results


@router.post("/import", response_model=MediaAssetResponse)
async def import_media(file: UploadFile = File(...)) -> MediaAssetResponse:
    """Import media file (video or PDF) and persist into raw storage."""
    contents = await file.read()
    file_size = len(contents)
    sha256 = hashlib.sha256(contents).hexdigest()

    ext = (file.filename or "").split(".")[-1].lower()
    file_type = "pdf" if ext == "pdf" else "video" if ext in ["mp4", "mov", "mkv", "avi"] else "audio"

    asset_id = f"asset_{uuid.uuid4().hex[:8]}"
    save_path = settings.raw_dir / f"{asset_id}_{file.filename}"
    with open(save_path, "wb") as f:
        f.write(contents)

    metadata = {"original_name": file.filename, "content_type": file.content_type}
    duration_sec = 600.0 if file_type == "video" else None
    page_count = 10 if file_type == "pdf" else None

    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO media_assets (id, filename, file_type, file_path, file_size_bytes, duration_sec, page_count, sha256_hash, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                asset_id,
                file.filename or "unknown",
                file_type,
                str(save_path),
                file_size,
                duration_sec,
                page_count,
                sha256,
                json.dumps(metadata),
            ),
        )
        conn.commit()

    return MediaAssetResponse(
        id=asset_id,
        filename=file.filename or "unknown",
        file_type=file_type,
        file_path=str(save_path),
        file_size_bytes=file_size,
        duration_sec=duration_sec,
        page_count=page_count,
        sha256_hash=sha256,
        metadata=metadata,
        created_at="just now",
    )
