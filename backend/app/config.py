"""Parallax Configuration & macOS Runtime Path Resolution.

Handles persistent user data routing to ~/Library/Application Support/Parallax/
when frozen as a macOS .app bundle, while supporting clean local development.
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path
from typing import Optional


def is_frozen() -> bool:
    """Return True if executing inside a frozen PyInstaller application bundle."""
    return getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")


def get_base_bundle_dir() -> Path:
    """Return the PyInstaller temporary extraction directory or repo root."""
    if is_frozen():
        return Path(getattr(sys, "_MEIPASS"))
    # In dev, repo root is two levels up from backend/app/
    return Path(__file__).resolve().parent.parent.parent


def get_storage_root() -> Path:
    """Resolve the storage directory for all mutable state.

    - When frozen in Parallax.app: ~/Library/Application Support/Parallax/
    - When running locally in dev: ./data or PARALLAX_DATA_DIR env var
    """
    env_dir = os.getenv("PARALLAX_DATA_DIR")
    if env_dir:
        return Path(env_dir).expanduser().resolve()

    if is_frozen():
        app_support = Path.home() / "Library" / "Application Support" / "Parallax"
        return app_support

    # Local development default
    return get_base_bundle_dir() / "data"


class AppSettings:
    """Application settings with deterministic path resolution."""

    def __init__(self, storage_dir: Optional[Path] = None):
        self.storage_root: Path = storage_dir or get_storage_root()
        self.db_path: Path = self.storage_root / "parallax.db"
        self.lancedb_dir: Path = self.storage_root / "lancedb"
        self.raw_dir: Path = self.storage_root / "raw"
        self.processed_dir: Path = self.storage_root / "processed"
        self.exports_dir: Path = self.storage_root / "exports"
        self.ensure_directories()

    def ensure_directories(self) -> None:
        """Create mutable storage directories on disk if they do not exist."""
        for directory in [
            self.storage_root,
            self.lancedb_dir,
            self.raw_dir,
            self.processed_dir,
            self.exports_dir,
        ]:
            directory.mkdir(parents=True, exist_ok=True)

    def get_ffmpeg_binary(self) -> str:
        """Resolve the ffmpeg binary location.

        1. If frozen: check sys._MEIPASS/ffmpeg or sys._MEIPASS/bin/ffmpeg
        2. Fallback: system PATH via shutil.which('ffmpeg')
        """
        if is_frozen():
            bundle_dir = get_base_bundle_dir()
            bundled_candidates = [
                bundle_dir / "ffmpeg",
                bundle_dir / "bin" / "ffmpeg",
                bundle_dir / "packaging" / "ffmpeg",
            ]
            for candidate in bundled_candidates:
                if candidate.is_file() and os.access(candidate, os.X_OK):
                    return str(candidate)

        which_ffmpeg = shutil.which("ffmpeg")
        if which_ffmpeg:
            return which_ffmpeg

        # Fallback to local user bin if present
        local_bin = Path.home() / ".local" / "bin" / "ffmpeg"
        if local_bin.is_file() and os.access(local_bin, os.X_OK):
            return str(local_bin)

        return "ffmpeg"

    def get_schema_path(self) -> Path:
        """Resolve schema.sql from the frozen bundle or source tree."""
        bundle_dir = get_base_bundle_dir()
        candidates = [
            bundle_dir / "backend" / "app" / "db" / "schema.sql",
            bundle_dir / "app" / "db" / "schema.sql",
            bundle_dir / "db" / "schema.sql",
            Path(__file__).resolve().parent / "db" / "schema.sql",
        ]
        for c in candidates:
            if c.is_file():
                return c
        return candidates[0]

    def get_frontend_dist_dir(self) -> Optional[Path]:
        """Resolve the frontend/dist directory for static serving."""
        bundle_dir = get_base_bundle_dir()
        candidates = [
            bundle_dir / "frontend" / "dist",
            bundle_dir / "dist" / "frontend",
            Path(__file__).resolve().parent.parent.parent / "frontend" / "dist",
        ]
        for c in candidates:
            if c.is_dir() and (c / "index.html").is_file():
                return c
        return None


settings = AppSettings()
