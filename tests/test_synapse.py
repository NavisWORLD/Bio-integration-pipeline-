import json
from pathlib import Path
import unittest

from cosmos_bio_cns.synapse import SynapticFeature, cosmos_12d_step, synaptic_step


class SynapseParityTests(unittest.TestCase):
    def test_matches_golden_vector(self):
        golden = json.loads(Path("sdk/spec/golden_vector.json").read_text(encoding="utf-8"))
        state = tuple(golden["previous_state"])
        features = [SynapticFeature(**feature) for feature in golden["features"]]
        actual = synaptic_step(state, features, leak=golden["leak"], input_gain=golden["input_gain"])
        for value, expected in zip(actual, golden["expected_state"]):
            self.assertAlmostEqual(value, expected, places=12)

    def test_empty_feature_set_preserves_state(self):
        state = tuple(float(i) / 20.0 for i in range(12))
        self.assertEqual(cosmos_12d_step(state, []), state)

    def test_quality_validation(self):
        with self.assertRaises(ValueError):
            SynapticFeature(0.5, 1.5)


if __name__ == "__main__":
    unittest.main()
