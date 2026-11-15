"""SQLite Database Management with WAL Mode & Row Serialization."""

from __future__ import annotations

import contextlib
import sqlite3
from pathlib import Path
from typing import Generator, Optional

from backend.app.config import settings


def init_db(db_path: Optional[Path] = None, schema_path: Optional[Path] = None) -> None:
    """Initialize SQLite database with WAL mode and execute schema.sql."""
    target_db = db_path or settings.db_path
    target_schema = schema_path or settings.get_schema_path()

    target_db.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(target_db, timeout=20.0) as conn:
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        conn.execute("PRAGMA foreign_keys = ON;")

        if target_schema.is_file():
            with open(target_schema, "r", encoding="utf-8") as f:
                conn.executescript(f.read())
        conn.commit()


@contextlib.contextmanager
def get_db(db_path: Optional[Path] = None) -> Generator[sqlite3.Connection, None, None]:
    """Yield a connection configured with Row factory and busy timeout."""
    target_db = db_path or settings.db_path
    conn = sqlite3.connect(target_db, timeout=20.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
    finally:
        conn.close()


def check_wal_status(db_path: Optional[Path] = None) -> str:
    """Return the active SQLite journal mode."""
    target_db = db_path or settings.db_path
    if not target_db.is_file():
        return "UNINITIALIZED"
    try:
        with sqlite3.connect(target_db, timeout=5.0) as conn:
            mode = conn.execute("PRAGMA journal_mode;").fetchone()[0]
            return str(mode).upper()
    except Exception:
        return "ERROR"
