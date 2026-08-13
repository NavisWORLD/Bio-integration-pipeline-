from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sqlite3
from typing import Any


class SQLiteEventStore:
    """Append-only event ledger with a SHA-256 hash chain."""

    def __init__(self, path: str | Path = "cosmos_bio_cns.sqlite3") -> None:
        self.path = str(path)
        self._db = sqlite3.connect(self.path)
        self._db.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                payload TEXT NOT NULL,
                previous_hash TEXT NOT NULL,
                event_hash TEXT NOT NULL UNIQUE,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self._db.commit()

    def append(self, event_type: str, payload: dict[str, Any]) -> str:
        previous_hash = self.head_hash()
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        digest = hashlib.sha256(f"{previous_hash}|{event_type}|{canonical}".encode()).hexdigest()
        self._db.execute(
            "INSERT INTO events(event_type, payload, previous_hash, event_hash) VALUES(?,?,?,?)",
            (event_type, canonical, previous_hash, digest),
        )
        self._db.commit()
        return digest

    def head_hash(self) -> str:
        row = self._db.execute("SELECT event_hash FROM events ORDER BY id DESC LIMIT 1").fetchone()
        return row[0] if row else "GENESIS"

    def count(self) -> int:
        return int(self._db.execute("SELECT COUNT(*) FROM events").fetchone()[0])

    def verify(self) -> bool:
        previous = "GENESIS"
        rows = self._db.execute(
            "SELECT event_type, payload, previous_hash, event_hash FROM events ORDER BY id ASC"
        ).fetchall()
        for event_type, payload, previous_hash, event_hash in rows:
            if previous_hash != previous:
                return False
            digest = hashlib.sha256(f"{previous}|{event_type}|{payload}".encode()).hexdigest()
            if digest != event_hash:
                return False
            previous = event_hash
        return True

    def close(self) -> None:
        self._db.close()
