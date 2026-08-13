from __future__ import annotations

from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from typing import Any

from cosmos_bio_cns.adapters.push import PushBioAdapter
from cosmos_bio_cns.models import BioObservation, ConsentScope
from cosmos_bio_cns.persistence import SQLiteEventStore
from cosmos_bio_cns.runtime import BioCNSRuntime


class LocalCNSServer:
    """Small localhost JSON bridge for non-Python applications."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8765, db: str = "cosmos_bio_cns.sqlite3") -> None:
        self.host = host
        self.port = port
        self.store = SQLiteEventStore(db)
        self.adapter = PushBioAdapter()
        self.runtime = BioCNSRuntime([self.adapter], store=self.store)
        self.runtime.start()
        self.last_frame = None
        self.last_state = None
        parent = self

        class Handler(BaseHTTPRequestHandler):
            server_version = "COSMOSBioCNS/0.1"

            def _json(self, status: int, payload: dict[str, Any]) -> None:
                body = json.dumps(payload, sort_keys=True).encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(body)

            def do_GET(self) -> None:
                if self.path == "/health":
                    self._json(200, {"ok": True, "service": "cosmos-bio-cns", "ledger_valid": parent.store.verify()})
                    return
                if self.path == "/v1/state":
                    self._json(200, {
                        "frame": asdict(parent.last_frame) if parent.last_frame else None,
                        "state": asdict(parent.last_state) if parent.last_state else None,
                    })
                    return
                if self.path == "/v1/ledger/verify":
                    self._json(200, {"events": parent.store.count(), "head": parent.store.head_hash(), "valid": parent.store.verify()})
                    return
                self._json(404, {"error": "not_found"})

            def do_POST(self) -> None:
                if self.path != "/v1/observe":
                    self._json(404, {"error": "not_found"})
                    return
                try:
                    length = int(self.headers.get("Content-Length", "0"))
                    raw = self.rfile.read(length)
                    data = json.loads(raw or b"{}")
                    items = data if isinstance(data, list) else [data]
                    observations = [self._parse_observation(item) for item in items]
                    parent.adapter.extend(observations)
                    frame, state = parent.runtime.step()
                    parent.last_frame = frame
                    parent.last_state = state
                    self._json(200, {"frame": asdict(frame), "state": asdict(state)})
                except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
                    self._json(400, {"error": "invalid_observation", "detail": str(exc)})
                except Exception as exc:
                    self._json(500, {"error": "runtime_error", "detail": str(exc)})

            @staticmethod
            def _parse_observation(item: dict[str, Any]) -> BioObservation:
                if not isinstance(item, dict):
                    raise TypeError("each observation must be an object")
                consent_data = item.get("consent")
                consent = ConsentScope(**consent_data) if isinstance(consent_data, dict) else None
                allowed = {
                    "sensor", "channel", "value", "unit", "quality", "timestamp", "sequence",
                    "subject_id", "device_id", "metadata"
                }
                kwargs = {key: value for key, value in item.items() if key in allowed}
                kwargs["consent"] = consent
                return BioObservation(**kwargs)

            def log_message(self, fmt: str, *args: Any) -> None:
                return

        self._httpd = ThreadingHTTPServer((self.host, self.port), Handler)

    def serve_forever(self) -> None:
        try:
            self._httpd.serve_forever()
        finally:
            self.close()

    def close(self) -> None:
        self._httpd.server_close()
        self.runtime.stop()
        self.store.close()
