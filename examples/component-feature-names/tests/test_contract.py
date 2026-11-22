"""Command contract for #679 component-local feature-name namespaces."""

import unittest
from pathlib import Path

from scpf.runner import run_script


ROOT = Path(__file__).resolve().parents[3]
MODEL = ROOT / "examples/component-feature-names/scpf/model.py"


class ComponentFeatureNameContractTests(unittest.TestCase):
    def test_native_feature_names_are_unique_per_component_definition(self):
        commands = run_script(MODEL)["commands"]

        sketches = [
            row["params"]["name"]
            for row in commands
            if row["command"] == "sketch.create"
        ]
        extrusions = [
            row["params"]["name"]
            for row in commands
            if row["command"] == "solid.extrude"
        ]

        self.assertEqual(
            sketches,
            [
                "d1_LeftPanel_Profile",
                "d2_RightPanel_Profile",
                "d3_Strip_Profile",
                "d4_Strip_2_Profile",
            ],
        )
        self.assertEqual(extrusions, sketches)
        self.assertEqual(len(sketches), len(set(sketches)))


if __name__ == "__main__":
    unittest.main()
