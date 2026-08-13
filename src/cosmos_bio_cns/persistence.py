from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sqlite3
from threading import RLock
from typing import Any


class SQLiteEventStore:
    """Append-only event ledger with a SHA-256 hash chain.

    The connection is configured for use by the threaded local HTTP bridge and
    all database operations are serialized with an RLock. This keeps one event
    chain deterministic even when multiple request threads publish events.
    """

    def __init__(self, path: str | Path = "cosmos_bio_cns.sqlite3") -> None:
        self.path = str(path)
        self._lock = RLock()
        self._db = sqlite3.connect(self.path, check_same_thread=False)
        with self._lock:
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

    def _head_hash_unlocked(self) -> str:
        row = self._db.execute("SELECT event_hash FROM events ORDER BY id DESC LIMIT 1").fetchone()
        return row[0] if row else "GENESIS"

    def append(self, event_type: str, payload: dict[str, Any]) -> str:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        with self._lock:
            previous_hash = self._head_hash_unlocked()
            digest = hashlib.sha256(f"{previous_hash}|{event_type}|{canonical}".encode()).hexdigest()
            self._db.execute(
                "INSERT INTO events(event_type, payload, previous_hash, event_hash) VALUES(?,?,?,?)",
                (event_type, canonical, previous_hash, digest),
            )
            self._db.commit()
            return digest

    def head_hash(self) -> str:
        with self._lock:
            return self._head_hash_unlocked()

    def count(self) -> int:
        with self._lock:
            return int(self._db.execute("SELECT COUNT(*) FROM events").fetchone()[0])

    def verify(self) -> bool:
        with self._lock:
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
        with self._lock:
            self._db.close()
