"""Command contract for #753 HUB75-style component history."""

from pathlib import Path
import unittest

from scpf.runner import run_script


ROOT = Path(__file__).resolve().parents[3]
MODEL = ROOT / "examples/component-cylinder-occurrence/scpf/model.py"


class ComponentCylinderOccurrenceContractTests(unittest.TestCase):
    def setUp(self):
        self.commands = run_script(MODEL)["commands"]

    def of(self, kind):
        return [
            row["params"]
            for row in self.commands
            if row["command"] == kind
        ]

    def test_fixture_preserves_real_multi_feature_history_shape(self):
        self.assertEqual(len(self.of("component.create")), 1)
        self.assertEqual(len(self.of("solid.loft")), 1)
        self.assertEqual(len(self.of("solid.cylinder")), 14)
        self.assertEqual(len(self.of("solid.hole")), 24)
        self.assertEqual(len(self.of("occurrence.copy")), 4)
        self.assertEqual(len(self.of("occurrence.move")), 5)

        cylinders = self.of("solid.cylinder")
        self.assertTrue(all(row["operation"] == "join" for row in cylinders))
        self.assertTrue(all(
            row["targets"] == ["Hub75HistoryPanel"]
            for row in cylinders
        ))

    def test_component_history_finishes_before_occurrence_copies(self):
        last_cylinder = max(
            i for i, row in enumerate(self.commands)
            if row["command"] == "solid.cylinder"
        )
        last_hole = max(
            i for i, row in enumerate(self.commands)
            if row["command"] == "solid.hole"
        )
        root_index = next(
            i for i, row in enumerate(self.commands)
            if row["command"] == "component.activate"
            and row["params"]["component"] == "root"
        )
        copy_index = next(
            i for i, row in enumerate(self.commands)
            if row["command"] == "occurrence.copy"
        )

        self.assertLess(last_cylinder, root_index)
        self.assertLess(last_hole, root_index)
        self.assertLess(root_index, copy_index)

    def test_five_occurrences_use_product_rotation_mix(self):
        moves = self.of("occurrence.move")
        self.assertEqual(
            [row["occurrence"] for row in moves],
            [f"$hub75historypanel_occurrence_{i}" for i in range(1, 6)],
        )
        self.assertEqual(
            [row["translate"] for row in moves],
            [
                [0, 0, 160.0],
                [-320.0, 0, 160.0],
                [-160.0, 0, 160.0],
                [160.0, 0, 160.0],
                [320.0, 0, 160.0],
            ],
        )
        for i, move in enumerate(moves):
            if i in (2, 3):
                self.assertEqual(move["axis"], [0.0, 1.0, -1.0])
                self.assertEqual(move["angle"], "180 deg")
            else:
                self.assertEqual(move["axis"], [1.0, 0.0, 0.0])
                self.assertEqual(move["angle"], "90 deg")


if __name__ == "__main__":
    unittest.main()
