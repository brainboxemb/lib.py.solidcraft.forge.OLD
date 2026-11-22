"""Unit contracts for the first native sheet-metal workflow."""

import unittest

from scpf import Anchor, Box, Hole, Parameter, Rectangle2D, Sketch
from scpf.compiler import ModelError, compile_model


def make_sheet(
    *,
    thickness=2,
    bend_radius=2,
    k_factor=0.5,
    fold_angle=90,
):
    with Sketch(name="Blank", plane="XY") as blank:
        Rectangle2D(80, 40)

    sheet = blank.sheet_metal(
        thickness=thickness,
        bend_radius=bend_radius,
        k_factor=k_factor,
        rule_name="Qualification Sheet",
    )
    sheet = sheet + Hole(
        d=6,
        direction=(0, 0, -1),
    ).at(-20, 0, thickness)
    return sheet.fold(
        line=((20, -20), (20, 20)),
        angle=fold_angle,
        fixed=(-30, 0, 0),
    )


class SheetMetalTests(unittest.TestCase):
    def test_blank_hole_and_fold_lower_to_native_sheet_history(self):
        document = compile_model(make_sheet(), "SheetFold")
        commands = document["commands"]

        self.assertEqual(
            [row["command"] for row in commands],
            [
                "sheet.manage_rules",
                "sketch.create",
                "sketch.rectangle.two_point",
                "sketch.finish",
                "sheet.flange",
                "solid.hole",
                "sheet.fold",
            ],
        )

        rule = commands[0]["params"]
        self.assertEqual(
            rule,
            {
                "name": "Qualification Sheet",
                "thickness": 2,
                "k_factor": 0.5,
                "bend_radius": 2,
                "active": True,
            },
        )

        base = commands[4]["params"]
        self.assertEqual(
            base,
            {
                "type": "base",
                "sketch": "Blank",
                "rule": "Qualification Sheet",
                "body_name": "SheetFold",
            },
        )

        hole = commands[5]["params"]
        self.assertEqual(hole["position"], [-20, 0, 2])
        self.assertEqual(hole["diameter"], 6)
        self.assertEqual(hole["direction"], [0, 0, -1])
        self.assertEqual(hole["targets"], ["SheetFold"])

        fold = commands[6]["params"]
        self.assertEqual(
            fold,
            {
                "points": [[20, -20, 0], [20, 20, 0]],
                "angle": 90,
                "position": "centerline",
                "flip": False,
                "body": "SheetFold",
                "fixed": [-30, 0, 0],
            },
        )

        self.assertFalse(
            any(row["command"] == "solid.extrude" for row in commands)
        )

    def test_sheet_rule_and_fold_parameter_units_are_correct(self):
        thickness = Parameter("thickness", 2)
        radius = Parameter("bend_radius", 2)
        k_factor = Parameter("k_factor", 0.5)
        angle = Parameter("bend_angle", 90)

        commands = compile_model(
            make_sheet(
                thickness=thickness,
                bend_radius=radius,
                k_factor=k_factor,
                fold_angle=angle,
            ),
            "SheetFold",
        )["commands"]

        units = {
            row["params"]["name"]: row["params"]["unit"]
            for row in commands
            if row["command"] == "parameters.add"
        }
        self.assertEqual(
            units,
            {
                "thickness": "mm",
                "bend_radius": "mm",
                "k_factor": "",
                "bend_angle": "deg",
            },
        )

        rule = next(
            row["params"]
            for row in commands
            if row["command"] == "sheet.manage_rules"
        )
        self.assertEqual(rule["thickness"], "thickness")
        self.assertEqual(rule["bend_radius"], "bend_radius")
        self.assertEqual(rule["k_factor"], "k_factor")

        fold = next(
            row["params"]
            for row in commands
            if row["command"] == "sheet.fold"
        )
        self.assertEqual(fold["angle"], "bend_angle")

    def test_connected_profile_is_shared_by_sheet_metal_base(self):
        with Sketch(name="MixedBlank", plane="XY") as blank:
            contour = blank.profile(start=(0, 0))
            contour.line_to((40, 0))
            contour.arc_through_to((40, 20), through=(50, 10))
            contour.line_to((0, 20))
            contour.line_to((0, 0))
            contour.close()

        commands = compile_model(
            blank.sheet_metal(
                thickness=2,
                bend_radius=2,
                rule_name="Mixed Sheet",
            ),
            "MixedSheet",
        )["commands"]
        self.assertEqual(
            [row["command"] for row in commands],
            [
                "sheet.manage_rules",
                "sketch.create",
                "sketch.line",
                "sketch.arc.three_point",
                "sketch.line",
                "sketch.line",
                "sketch.finish",
                "sheet.flange",
            ],
        )
        for row in commands[2:6]:
            self.assertTrue(row["params"]["connect"])

    def test_native_edge_flange_inherits_sheet_rule(self):
        with Sketch(name="Blank", plane="XY") as blank:
            Rectangle2D(80, 40)

        sheet = blank.sheet_metal(
            thickness=2,
            bend_radius=2,
            k_factor=0.5,
            rule_name="Edge Flange Rule",
        )
        flanged = sheet.flange(
            edges=[(40, 0, 2)],
            height=18,
        )
        commands = compile_model(flanged, "EdgeFlange")["commands"]

        self.assertEqual(
            [row["command"] for row in commands],
            [
                "sheet.manage_rules",
                "sketch.create",
                "sketch.rectangle.two_point",
                "sketch.finish",
                "sheet.flange",
                "sheet.flange",
            ],
        )
        edge = commands[-1]["params"]
        self.assertEqual(
            edge,
            {
                "type": "edge",
                "edges": [[40.0, 0.0, 2.0]],
                "height": 18,
                "angle": 90,
                "body": "EdgeFlange",
            },
        )
        self.assertNotIn("thickness", edge)
        self.assertNotIn("k_factor", edge)
        self.assertNotIn("radius", edge)
        self.assertEqual(commands[4]["params"]["type"], "base")
        self.assertEqual(commands[4]["params"]["rule"], "Edge Flange Rule")

    def test_edge_flange_parameter_units_and_native_options(self):
        height = Parameter("flange_height", 18)
        angle = Parameter("flange_angle", 95)

        with Sketch(name="Blank", plane="XY") as blank:
            Rectangle2D(80, 40)

        sheet = blank.sheet_metal(
            thickness=2,
            bend_radius=2,
            rule_name="Edge Flange Rule",
        )
        commands = compile_model(
            sheet.flange(
                edges=[(40, -10, 2), (40, 10, 2)],
                height=height,
                angle=angle,
                height_from="inner",
                position="material_outside",
                flip=True,
            ),
            "ParametricEdgeFlange",
        )["commands"]

        units = {
            row["params"]["name"]: row["params"]["unit"]
            for row in commands
            if row["command"] == "parameters.add"
        }
        self.assertEqual(units["flange_height"], "mm")
        self.assertEqual(units["flange_angle"], "deg")

        edge = commands[-1]["params"]
        self.assertEqual(edge["height"], "flange_height")
        self.assertEqual(edge["angle"], "flange_angle")
        self.assertEqual(
            edge["edges"],
            [[40.0, -10.0, 2.0], [40.0, 10.0, 2.0]],
        )
        self.assertEqual(edge["height_from"], "inner")
        self.assertEqual(edge["position"], "material_outside")
        self.assertTrue(edge["flip"])

    def test_edge_flange_validates_public_contract(self):
        with Sketch(name="Blank", plane="XY") as blank:
            Rectangle2D(80, 40)
        sheet = blank.sheet_metal(thickness=2, bend_radius=2)

        invalid_edges = (
            [],
            [(0, 0)],
            [(0, 0, 0, 0)],
            [(True, 0, 0)],
            [(float("nan"), 0, 0)],
            [(Parameter("edge_x", 40), 0, 2)],
        )
        for edges in invalid_edges:
            with self.subTest(edges=edges), self.assertRaises(ValueError):
                sheet.flange(edges=edges, height=10)

        for height in (0, -1, float("nan")):
            with self.subTest(height=height), self.assertRaisesRegex(
                ValueError, "height"
            ):
                sheet.flange(edges=[(40, 0, 2)], height=height)

        for angle in (0, 180, -180, float("nan")):
            with self.subTest(angle=angle), self.assertRaisesRegex(
                ValueError, "angle"
            ):
                sheet.flange(edges=[(40, 0, 2)], height=10, angle=angle)

        with self.assertRaisesRegex(ValueError, "height_from"):
            sheet.flange(
                edges=[(40, 0, 2)],
                height=10,
                height_from="middle",
            )
        with self.assertRaisesRegex(ValueError, "position"):
            sheet.flange(
                edges=[(40, 0, 2)],
                height=10,
                position="center",
            )
        with self.assertRaisesRegex(TypeError, "flip"):
            sheet.flange(
                edges=[(40, 0, 2)],
                height=10,
                flip="yes",
            )

        ordinary = Box(80, 40, 2, anchor=Anchor.BOTTOM)
        with self.assertRaisesRegex(ModelError, "existing sheet material"):
            compile_model(
                ordinary.flange(edges=[(40, 0, 2)], height=10),
                "NotSheet",
            )

    def test_sheet_metal_and_fold_validate_authoring_contract(self):
        with Sketch(name="Blank", plane="XY") as blank:
            Rectangle2D(80, 40)

        with self.assertRaisesRegex(ValueError, "thickness"):
            blank.sheet_metal(thickness=0, bend_radius=2)
        with self.assertRaisesRegex(ValueError, "bend_radius"):
            blank.sheet_metal(thickness=2, bend_radius=0)
        with self.assertRaisesRegex(ValueError, "k_factor"):
            blank.sheet_metal(thickness=2, bend_radius=2, k_factor=1)
        with self.assertRaisesRegex(ValueError, "rule_name"):
            blank.sheet_metal(
                thickness=2,
                bend_radius=2,
                rule_name="",
            )

        sheet = blank.sheet_metal(thickness=2, bend_radius=2)
        with self.assertRaisesRegex(ValueError, "exactly two"):
            sheet.fold(line=((0, 0),), angle=90)
        with self.assertRaisesRegex(ValueError, "different"):
            sheet.fold(line=((0, 0), (0, 0)), angle=90)
        with self.assertRaisesRegex(ValueError, "angle"):
            sheet.fold(line=((0, -10), (0, 10)), angle=0)
        with self.assertRaisesRegex(ValueError, "position"):
            sheet.fold(
                line=((0, -10), (0, 10)),
                position="outside",
            )

        with self.assertRaisesRegex(ValueError, "fixed numbers"):
            sheet.fold(
                line=((Parameter("fold_x", 20), -10), (20, 10)),
            )


if __name__ == "__main__":
    unittest.main()
