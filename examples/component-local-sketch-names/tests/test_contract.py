"""Command contract for #679 component-local Sketch feature identity."""

import unittest
from pathlib import Path

from scpf.runner import run_script


ROOT = Path(__file__).resolve().parents[3]
MODEL = ROOT / "examples/component-local-sketch-names/scpf/model.py"


class ComponentLocalSketchNameContractTests(unittest.TestCase):
    def test_independent_components_get_distinct_native_sketch_names(self):
        commands = run_script(MODEL)["commands"]
        sketch_names = [
            row["params"]["name"]
            for row in commands
            if row["command"] == "sketch.create"
        ]
        self.assertEqual(
            sketch_names,
            [
                "d1_LeftPlate__Profile",
                "d2_RightPlate__Profile",
            ],
        )
        self.assertEqual(len(sketch_names), len(set(sketch_names)))

    def test_feature_namespacing_does_not_require_consumer_prefixes(self):
        source = MODEL.read_text(encoding="utf-8")
        self.assertEqual(source.count('Sketch(name="Profile"'), 2)
        self.assertNotIn("d1_", source)
        self.assertNotIn("d2_", source)


if __name__ == "__main__":
    unittest.main()
