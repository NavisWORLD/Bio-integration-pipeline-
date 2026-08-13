import unittest
from cosmos_bio_cns.baseline import RunningBaseline


class BaselineTests(unittest.TestCase):
    def test_baseline_moves_and_is_finite(self):
        b = RunningBaseline(alpha=0.2)
        self.assertEqual(b.update(70.0), 0.0)
        z = b.update(80.0)
        self.assertTrue(abs(z) < 10)
        self.assertGreater(b.mean, 70.0)


if __name__ == "__main__":
    unittest.main()
