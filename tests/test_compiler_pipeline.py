"""Tests for 60fps Forensic Video Expose Compiler."""

from pathlib import Path

from backend.app.models.schemas import ExposeCompileRequest
from backend.app.services.compiler import VideoCompiler


def test_compile_expose(temp_storage, monkeypatch):
    """Compiler must output a valid MP4 file with non-zero size."""
    monkeypatch.setattr("backend.app.services.compiler.settings", temp_storage)

    req = ExposeCompileRequest(
        contradiction_ids=["contra_01"],
        fps=60,
        resolution="1920x1080",
        split_screen_layout="side_by_side",
    )

    resp = VideoCompiler.compile_expose(req)
    assert resp.success is True
    assert resp.fps == 60
    assert Path(resp.output_path).is_file()
    assert resp.file_size_bytes > 0
