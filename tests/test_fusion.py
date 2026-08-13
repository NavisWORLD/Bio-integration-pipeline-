import unittest

from cosmos_bio_cns.fusion import BioFusionEngine
from cosmos_bio_cns.models import BioObservation, ConsentScope


class FusionTests(unittest.TestCase):
    def test_processing_consent_is_enforced(self):
        engine = BioFusionEngine()
        denied = BioObservation(
            sensor="watch",
            channel="heart_rate",
            value=72.0,
            unit="bpm",
            quality=1.0,
            consent=ConsentScope(session_id="s1", bio_processing=False),
        )
        frame = engine.ingest([denied])
        self.assertEqual(frame.features, ())
        self.assertEqual(frame.confidence, 0.0)

    def test_baselines_are_isolated_by_sensor_and_unit(self):
        engine = BioFusionEngine(alpha=0.5)
        engine.ingest([
            BioObservation(sensor="watch-a", channel="heart_rate", value=60.0, unit="bpm", quality=1.0),
            BioObservation(sensor="watch-b", channel="heart_rate", value=1.0, unit="hz", quality=1.0),
        ])
        frame = engine.ingest([
            BioObservation(sensor="watch-a", channel="heart_rate", value=90.0, unit="bpm", quality=1.0),
            BioObservation(sensor="watch-b", channel="heart_rate", value=1.0, unit="hz", quality=1.0),
        ])
        self.assertGreater(abs(frame.features[0].baseline_delta), 0.1)
        self.assertAlmostEqual(frame.features[1].baseline_delta, 0.0, places=7)


if __name__ == "__main__":
    unittest.main()
