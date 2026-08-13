import unittest
from cosmos_bio_cns.cns import LocalCNS
from cosmos_bio_cns.models import BioFeature, FusionFrame


class CNSTests(unittest.TestCase):
    def test_deterministic_update(self):
        frame = FusionFrame(
            features=(BioFeature(channel="heart_rate", name="heart_rate", value=80, quality=1.0, baseline_delta=1.0),),
            confidence=1.0,
            window_ms=1000,
        )
        a = LocalCNS()
        b = LocalCNS()
        self.assertEqual(a.update(frame).vector, b.update(frame).vector)


if __name__ == "__main__":
    unittest.main()
