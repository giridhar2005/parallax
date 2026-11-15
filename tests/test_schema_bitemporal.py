"""Tests for Bi-Temporal SQLite WAL schema and integrity."""

from backend.app.db.database import check_wal_status, get_db


def test_sqlite_wal_mode(temp_storage):
    """Confirm database runs in SQLite WAL mode."""
    wal = check_wal_status(temp_storage.db_path)
    assert wal == "WAL"


def test_bitemporal_fixtures_loaded(temp_storage):
    """Verify seeded assets, claims, evidence, and contradictions exist."""
    with get_db(temp_storage.db_path) as conn:
        assets_cnt = conn.execute("SELECT COUNT(*) FROM media_assets").fetchone()[0]
        claims_cnt = conn.execute("SELECT COUNT(*) FROM claims").fetchone()[0]
        ev_cnt = conn.execute("SELECT COUNT(*) FROM evidence_nodes").fetchone()[0]
        contra_cnt = conn.execute("SELECT COUNT(*) FROM contradictions").fetchone()[0]

        assert assets_cnt >= 3
        assert claims_cnt >= 4
        assert ev_cnt >= 4
        assert contra_cnt >= 4


def test_foreign_key_cascade(temp_storage):
    """Deleting a claim must cascade-delete linked contradictions."""
    with get_db(temp_storage.db_path) as conn:
        claim_id = "claim_01"
        # Confirm contradiction exists
        linked = conn.execute("SELECT COUNT(*) FROM contradictions WHERE claim_id = ?", (claim_id,)).fetchone()[0]
        assert linked > 0

        # Delete claim
        conn.execute("DELETE FROM claims WHERE id = ?", (claim_id,))
        conn.commit()

        # Contradictions must be gone
        after = conn.execute("SELECT COUNT(*) FROM contradictions WHERE claim_id = ?", (claim_id,)).fetchone()[0]
        assert after == 0
