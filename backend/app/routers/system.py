"""System Status & Storage Telemetry Router."""

from __future__ import annotations

import shutil

from fastapi import APIRouter

from backend.app.config import is_frozen, settings
from backend.app.db.database import check_wal_status, get_db
from backend.app.models.schemas import SystemStatus
from backend.app.services.fixtures import seed_fixtures

router = APIRouter(prefix="/api/system", tags=["System"])


@router.get("/status", response_model=SystemStatus)
async def get_system_status() -> SystemStatus:
    """Return runtime telemetry, SQLite WAL status, FFmpeg path, and storage directory."""
    ffmpeg_bin = settings.get_ffmpeg_binary()
    ffmpeg_available = bool(shutil.which(ffmpeg_bin) or (settings.storage_root and ffmpeg_bin != "ffmpeg"))

    counts = {"media_assets": 0, "claims": 0, "evidence_nodes": 0, "contradictions": 0}
    try:
        with get_db() as conn:
            counts["media_assets"] = conn.execute("SELECT COUNT(*) FROM media_assets").fetchone()[0]
            counts["claims"] = conn.execute("SELECT COUNT(*) FROM claims").fetchone()[0]
            counts["evidence_nodes"] = conn.execute("SELECT COUNT(*) FROM evidence_nodes").fetchone()[0]
            counts["contradictions"] = conn.execute("SELECT COUNT(*) FROM contradictions").fetchone()[0]
    except Exception:
        pass

    return SystemStatus(
        version="1.0.0",
        app_name="Parallax",
        sqlite_wal="ACTIVE" if check_wal_status() == "WAL" else check_wal_status(),
        ffmpeg_available=ffmpeg_available,
        ffmpeg_path=ffmpeg_bin,
        storage_path=str(settings.storage_root),
        is_frozen=is_frozen(),
        counts=counts,
    )


@router.post("/seed")
async def trigger_seed():
    """Seed sample corporate fraud deposition fixture dataset."""
    result = seed_fixtures()
    return result
