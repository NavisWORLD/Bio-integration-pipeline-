import unittest
from cosmos_bio_cns import load_schema


class SchemaTests(unittest.TestCase):
    def test_packaged_observation_schema_loads(self):
        schema = load_schema("bio_observation")
        self.assertEqual(schema["title"], "COSMOS Bio Observation")
        self.assertIn("quality", schema["required"])

    def test_unknown_schema_is_explicit(self):
        with self.assertRaises(KeyError):
            load_schema("does-not-exist")


if __name__ == "__main__":
    unittest.main()
