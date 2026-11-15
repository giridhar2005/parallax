"""Tests for desktop runtime configuration and macOS Application Support path routing."""

import sys
from pathlib import Path

from backend.app.config import AppSettings, get_storage_root, is_frozen


def test_is_frozen_detection(monkeypatch):
    """Test PyInstaller bundle detection."""
    monkeypatch.delattr(sys, "frozen", raising=False)
    assert not is_frozen()

    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "_MEIPASS", "/tmp/_MEI12345", raising=False)
    assert is_frozen()


def test_frozen_storage_path(monkeypatch):
    """When frozen, storage must route to ~/Library/Application Support/Parallax/."""
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "_MEIPASS", "/Applications/Parallax.app/Contents/MacOS", raising=False)
    monkeypatch.delenv("PARALLAX_DATA_DIR", raising=False)

    storage = get_storage_root()
    expected = Path.home() / "Library" / "Application Support" / "Parallax"
    assert storage == expected


def test_dev_storage_path(monkeypatch):
    """When in local dev, storage resolves to data/ in repo or PARALLAX_DATA_DIR."""
    monkeypatch.delattr(sys, "frozen", raising=False)
    monkeypatch.setenv("PARALLAX_DATA_DIR", "/tmp/parallax_custom_data")

    storage = get_storage_root()
    assert storage.resolve() == Path("/tmp/parallax_custom_data").resolve()


def test_ensure_directories(tmp_path):
    """AppSettings must create all mutable subdirectories."""
    custom_dir = tmp_path / "app_support_test"
    settings = AppSettings(storage_dir=custom_dir)

    assert settings.storage_root.is_dir()
    assert settings.lancedb_dir.is_dir()
    assert settings.raw_dir.is_dir()
    assert settings.processed_dir.is_dir()
    assert settings.exports_dir.is_dir()


def test_ffmpeg_resolution(temp_storage):
    """AppSettings should resolve ffmpeg from system or bundled path."""
    ffmpeg_bin = temp_storage.get_ffmpeg_binary()
    assert isinstance(ffmpeg_bin, str)
    assert len(ffmpeg_bin) > 0
