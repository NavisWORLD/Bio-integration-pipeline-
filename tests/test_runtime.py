import tempfile
import unittest
from pathlib import Path

from cosmos_bio_cns import BioCNSRuntime, SQLiteEventStore
from cosmos_bio_cns.adapters import DeterministicCardiacAdapter


class RuntimeTests(unittest.TestCase):
    def test_pipeline_emits_state_and_heartbeat(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = SQLiteEventStore(Path(tmp) / "events.sqlite3")
            rt = BioCNSRuntime([DeterministicCardiacAdapter()], store=store)
            rt.start()
            try:
                frame, state = rt.step()
            finally:
                rt.stop()
            self.assertEqual(state.dimensions, 12)
            self.assertEqual(len(state.vector), 12)
            self.assertGreater(frame.confidence, 0.9)
            self.assertEqual(store.count(), 2)
            self.assertTrue(store.verify())
            store.close()


if __name__ == "__main__":
    unittest.main()
