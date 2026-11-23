"""Command contract for the #567 connected-profile native fixture."""

import unittest
from pathlib import Path

from scpf.runner import run_script


ROOT = Path(__file__).resolve().parents[3]
MODEL = ROOT / "examples/connected-profile-sheet/scpf/model.py"


class ConnectedProfileSheetContractTests(unittest.TestCase):
    def test_mixed_profile_uses_native_connected_line_arc_history(self):
        commands = run_script(MODEL)["commands"]
        geometry = [
            row for row in commands
            if row["command"] != "parameters.add"
        ]

        self.assertEqual(
            [row["command"] for row in geometry],
            [
                "sheet.manage_rules",
                "sketch.create",
                "sketch.line",
                "sketch.arc.center_point",
                "sketch.line",
                "sketch.arc.center_point",
                "sketch.finish",
                "sheet.flange",
            ],
        )

        curves = geometry[2:6]
        self.assertTrue(all(row["params"]["connect"] for row in curves))
        self.assertEqual(
            [row["command"] for row in curves],
            [
                "sketch.line",
                "sketch.arc.center_point",
                "sketch.line",
                "sketch.arc.center_point",
            ],
        )

        text = repr([row["params"] for row in curves])
        self.assertIn("half_span", text)
        self.assertIn("radius", text)

        base = geometry[-1]["params"]
        self.assertEqual(base["type"], "base")
        self.assertEqual(base["sketch"], "Connected blank")
        self.assertEqual(base["rule"], "Connected Profile Rule")
        self.assertEqual(base["body_name"], "ConnectedProfileSheet")

        self.assertNotIn(
            "sketch.line",
            [
                row["command"]
                for row in geometry
                if row["command"] == "sketch.line"
                and row["params"].get("closed") is True
            ],
        )


if __name__ == "__main__":
    unittest.main()
