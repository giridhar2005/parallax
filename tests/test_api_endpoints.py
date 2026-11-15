"""Tests for Parallax REST API Endpoints."""

import io


def test_health_endpoint(client):
    """GET /health must return status ok and SQLite WAL indicator."""
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["app"] == "Parallax"


def test_system_status_endpoint(client):
    """GET /api/system/status must report app version, storage, and WAL status."""
    resp = client.get("/api/system/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["version"] == "1.0.0"
    assert data["sqlite_wal"] == "ACTIVE"
    assert "storage_path" in data
    assert "counts" in data
    assert data["counts"]["claims"] >= 4


def test_media_endpoints(client):
    """GET /api/media/list and POST /api/media/import."""
    list_resp = client.get("/api/media/list")
    assert list_resp.status_code == 200
    media_items = list_resp.json()
    assert len(media_items) >= 3

    # Upload test
    fake_pdf = io.BytesIO(b"%PDF-1.4 ... forensic test exhibit ...")
    upload_resp = client.post(
        "/api/media/import",
        files={"file": ("test_exhibit.pdf", fake_pdf, "application/pdf")},
    )
    assert upload_resp.status_code == 200
    uploaded = upload_resp.json()
    assert uploaded["filename"] == "test_exhibit.pdf"
    assert uploaded["file_type"] == "pdf"


def test_contradictions_endpoint(client):
    """GET /api/analysis/contradictions."""
    resp = client.get("/api/analysis/contradictions")
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) >= 4
    top = items[0]
    assert "claim_statement" in top
    assert "evidence_text" in top
    assert top["nli_score"] >= 0.85


def test_bitemporal_graph_endpoint(client):
    """GET /api/graph/bitemporal."""
    resp = client.get("/api/graph/bitemporal")
    assert resp.status_code == 200
    graph = resp.json()
    assert "points" in graph
    assert "claims" in graph
    assert "contradictions" in graph
    assert len(graph["points"]) > 0


def test_compile_expose_endpoint(client):
    """POST /api/compile/expose."""
    resp = client.post(
        "/api/compile/expose",
        json={"fps": 60, "resolution": "1920x1080", "split_screen_layout": "side_by_side"},
    )
    assert resp.status_code == 200
    result = resp.json()
    assert result["success"] is True
    assert result["fps"] == 60
