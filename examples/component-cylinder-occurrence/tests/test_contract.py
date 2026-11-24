"""Command contract for #753 component-local Cylinder join placement."""

from pathlib import Path
import unittest

from scpf.runner import run_script


ROOT = Path(__file__).resolve().parents[3]
MODEL = ROOT / "examples/component-cylinder-occurrence/scpf/model.py"


class ComponentCylinderOccurrenceContractTests(unittest.TestCase):
    def test_native_cylinder_is_authored_before_returning_to_root(self):
        commands = run_script(MODEL)["commands"]

        cylinder_index = next(
            index for index, row in enumerate(commands)
            if row["command"] == "solid.cylinder"
        )
        root_index = next(
            index for index, row in enumerate(commands)
            if row["command"] == "component.activate"
            and row["params"]["component"] == "root"
        )
        copy_index = next(
            index for index, row in enumerate(commands)
            if row["command"] == "occurrence.copy"
        )

        cylinder = commands[cylinder_index]["params"]
        self.assertEqual(cylinder["diameter"], 4)
        self.assertEqual(cylinder["height"], 4)
        self.assertEqual(cylinder["axis"], "Z")
        self.assertEqual(cylinder["operation"], "join")
        self.assertEqual(cylinder["targets"], ["BossedPanel"])
        self.assertLess(cylinder_index, root_index)
        self.assertLess(root_index, copy_index)

    def test_both_occurrences_use_bound_rotated_moves(self):
        commands = run_script(MODEL)["commands"]
        copies = [
            row for row in commands
            if row["command"] == "occurrence.copy"
        ]
        moves = [
            row["params"] for row in commands
            if row["command"] == "occurrence.move"
        ]

        self.assertEqual(len(copies), 1)
        self.assertEqual(len(moves), 2)
        self.assertEqual(
            [move["translate"] for move in moves],
            [[-30.0, 0.0, 0.0], [30.0, 0.0, 0.0]],
        )
        self.assertTrue(all(move["axis"] == [1.0, 0.0, 0.0] for move in moves))
        self.assertTrue(all(move["angle"] == "90 deg" for move in moves))


if __name__ == "__main__":
    unittest.main()
