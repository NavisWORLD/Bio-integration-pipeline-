import unittest
from cosmos_bio_cns.adapters import PushBioAdapter
from cosmos_bio_cns.models import BioObservation


class PushAdapterTests(unittest.TestCase):
    def test_push_and_drain(self):
        adapter = PushBioAdapter()
        adapter.connect()
        obs = BioObservation(sensor="test", channel="x", value=1.0, unit="u", quality=1.0)
        adapter.push(obs)
        self.assertEqual(adapter.read(), [obs])
        self.assertEqual(adapter.read(), [])
        adapter.disconnect()


if __name__ == "__main__":
    unittest.main()
