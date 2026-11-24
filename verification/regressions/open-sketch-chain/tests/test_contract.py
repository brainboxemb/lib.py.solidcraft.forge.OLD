"""Command contract for the #683 open connected Sketch-chain fixture."""

import unittest
from pathlib import Path

from scpf.runner import run_script


CASE_ROOT = Path(__file__).resolve().parents[1]
MODEL = CASE_ROOT / "scpf/model.py"


class OpenSketchChainContractTests(unittest.TestCase):
    def test_open_chain_uses_native_line_tangent_arc_line_history(self):
        commands = run_script(MODEL)["commands"]
        geometry = [
            row for row in commands
            if row["command"] != "parameters.add"
        ]

        self.assertEqual(
            [row["command"] for row in geometry],
            [
                "sketch.create",
                "sketch.line",
                "sketch.arc.tangent",
                "sketch.line",
                "sketch.finish",
            ],
        )

        first = geometry[1]["params"]
        tangent = geometry[2]["params"]
        second = geometry[3]["params"]

        self.assertEqual(first["ids"], ["l1"])
        self.assertTrue(first["connect"])
        self.assertEqual(tangent["start"], "l1.end")
        self.assertEqual(tangent["curve"], "l1")
        self.assertEqual(tangent["end"], [50, 10])
        self.assertEqual(second["ids"], ["l2"])
        self.assertTrue(second["connect"])

        text = repr([first, tangent, second])
        self.assertIn("length", text)
        self.assertIn("end_height", text)

        self.assertFalse(
            any(
                row["params"].get("closed") is True
                for row in geometry
                if row["command"] == "sketch.line"
            )
        )


if __name__ == "__main__":
    unittest.main()
