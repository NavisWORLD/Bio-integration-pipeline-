from __future__ import annotations

from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import ipaddress
import json
from threading import Lock
from typing import Any

from cosmos_bio_cns.adapters.push import PushBioAdapter
from cosmos_bio_cns.models import BioObservation, ConsentScope
from cosmos_bio_cns.persistence import SQLiteEventStore
from cosmos_bio_cns.runtime import BioCNSRuntime


def _is_loopback_host(host: str) -> bool:
    if host.lower() == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


class LocalCNSServer:
    """Small local JSON bridge for non-Python applications.

    The service has no authentication layer. It therefore refuses non-loopback
    binds unless the caller explicitly opts in with ``allow_remote=True``.
    """

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 8765,
        db: str = "cosmos_bio_cns.sqlite3",
        *,
        allow_remote: bool = False,
    ) -> None:
        if not _is_loopback_host(host) and not allow_remote:
            raise ValueError(
                "refusing non-loopback bind without allow_remote=True; "
                "the reference HTTP bridge does not provide authentication"
            )

        self.host = host
        self.port = port
        self.store = SQLiteEventStore(db)
        self.adapter = PushBioAdapter()
        self.runtime = BioCNSRuntime([self.adapter], store=self.store)
        self.runtime.start()
        self.last_frame = None
        self.last_state = None
        self._runtime_lock = Lock()
        self._closed = False
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
                    # Runtime + push adapter represent one ordered state machine.
                    # Serialize request updates so concurrent HTTP calls cannot
                    # interleave state transitions or ledger ancestry.
                    with parent._runtime_lock:
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
        # Port 0 is useful for tests/embedding; expose the actual selected port.
        self.port = int(self._httpd.server_address[1])

    def serve_forever(self) -> None:
        try:
            self._httpd.serve_forever()
        finally:
            self.close()

    def shutdown(self) -> None:
        self._httpd.shutdown()

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        self._httpd.server_close()
        self.runtime.stop()
        self.store.close()
