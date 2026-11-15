"""Pytest Fixtures for Parallax Test Suite."""

import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend.app.config import AppSettings
from backend.app.db.database import init_db
from backend.app.main import create_app
from backend.app.services.fixtures import seed_fixtures


@pytest.fixture
def temp_storage(monkeypatch):
    """Create an isolated temporary storage directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir)
        test_settings = AppSettings(storage_dir=storage_path)
        monkeypatch.setattr("backend.app.config.settings", test_settings)
        monkeypatch.setattr("backend.app.db.database.settings", test_settings)
        monkeypatch.setattr("backend.app.services.compiler.settings", test_settings)
        monkeypatch.setattr("backend.app.services.nli.settings", test_settings, raising=False)
        init_db(db_path=test_settings.db_path)
        seed_fixtures(db_path=test_settings.db_path)
        yield test_settings


@pytest.fixture
def client(temp_storage, monkeypatch):
    """Provide a FastAPI TestClient bound to temporary test storage."""
    monkeypatch.setattr("backend.app.config.settings", temp_storage)
    monkeypatch.setattr("backend.app.routers.system.settings", temp_storage)
    monkeypatch.setattr("backend.app.routers.media.settings", temp_storage)
    monkeypatch.setattr("backend.app.services.compiler.settings", temp_storage)
    monkeypatch.setattr("backend.app.main.settings", temp_storage)

    app = create_app()
    with TestClient(app) as test_client:
        yield test_client
