import json
from pathlib import Path
import tempfile
from threading import Thread
import unittest
from urllib.request import Request, urlopen

from cosmos_bio_cns.server import LocalCNSServer


class ServerTests(unittest.TestCase):
    def test_http_observation_runs_on_worker_thread_and_persists(self):
        with tempfile.TemporaryDirectory() as tmp:
            server = LocalCNSServer(port=0, db=str(Path(tmp) / "bridge.sqlite3"))
            thread = Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                payload = json.dumps({
                    "sensor": "watch",
                    "channel": "heart_rate",
                    "value": 72.0,
                    "unit": "bpm",
                    "quality": 0.99,
                }).encode("utf-8")
                request = Request(
                    f"http://127.0.0.1:{server.port}/v1/observe",
                    data=payload,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urlopen(request, timeout=5) as response:
                    body = json.load(response)
                self.assertEqual(body["state"]["dimensions"], 12)

                with urlopen(f"http://127.0.0.1:{server.port}/v1/ledger/verify", timeout=5) as response:
                    ledger = json.load(response)
                self.assertTrue(ledger["valid"])
                self.assertEqual(ledger["events"], 2)
            finally:
                server.shutdown()
                thread.join(timeout=5)

    def test_remote_bind_requires_explicit_opt_in(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                LocalCNSServer(host="0.0.0.0", port=0, db=str(Path(tmp) / "bridge.sqlite3"))


if __name__ == "__main__":
    unittest.main()
