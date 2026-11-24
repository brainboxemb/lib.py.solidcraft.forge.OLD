"""Regression fixture for the real HUB75-style multi-feature history."""

MOUNTING_TUBE_OUTER_DIAMETER = 8.50
MOUNTING_TUBE_PROTRUSION = 0.50
MOUNTING_TUBE_RELIEF_CLEARANCE = 0.75
MOUNTING_TUBE_RELIEF_DEPTH = 0.80

REINFORCEMENT_OUTER_DIAMETER = 14.0
REINFORCEMENT_RECESS_DIAMETER = 10.0
REINFORCEMENT_RECESS_DEPTH = 2.50
REINFORCEMENT_HOLE_DIAMETER = 2.50
REINFORCEMENT_HOLE_DEPTH = 10.00
REINFORCEMENT_OFFSET = 11.0

LOCATOR_PIN_DIAMETER = 3.00
LOCATOR_PIN_PROTRUSION = 3.00
LOCATOR_PIN_X = 75.0
LOCATOR_PIN_Y = 110.0


class Hub75HistoryPanel:
    width = 159.70
    height = 319.71
    depth = 14.50
    front_depth = 2.00
    rear_inset = 1.25
    mount_x = 72.0
    mount_y = 152.0
    hole_diameter = 3.0
    rear_side_rail = 12.5
    rear_end_rail = 10.75
    rear_crossbar = 20.0

    def build(self):
        body = Box(
            self.width,
            self.height,
            self.depth,
            anchor=Anchor.BOTTOM,
        ).taper(
            from_z=self.front_depth,
            inset=self.rear_inset,
        )

        side = self.rear_side_rail * (159.70 / 160.0)
        end = self.rear_end_rail * (319.71 / 320.0)
        rib_half = half(self.rear_crossbar * (319.71 / 320.0))
        half_height = half(self.height)
        quarter_height = self.height / 4
        opening_width = self.width - 2 * side
        bay_ranges = (
            (-half_height + end, -quarter_height - rib_half),
            (-quarter_height + rib_half, -rib_half),
            (rib_half, quarter_height - rib_half),
            (quarter_height + rib_half, half_height - end),
        )
        with Sketch(
            name="Rear electronics bays",
            on=body,
            parent=Anchor.TOP,
        ) as bays:
            for bottom, top in bay_ranges:
                bays.add(
                    Rectangle2D(opening_width, top - bottom),
                    offset=(0, midpoint(bottom, top)),
                )
        body = body - bays.extrude(-(self.depth - self.front_depth))

        relief_diameter = (
            MOUNTING_TUBE_OUTER_DIAMETER
            + 2 * MOUNTING_TUBE_RELIEF_CLEARANCE
        )
        for x in (-self.mount_x, self.mount_x):
            for y in (-self.mount_y, 0, self.mount_y):
                body = body + Hole(
                    d=relief_diameter,
                    depth=MOUNTING_TUBE_RELIEF_DEPTH,
                    direction=(0, 0, -1),
                ).at(x, y, self.depth)

                body = body + Cylinder(
                    d=MOUNTING_TUBE_OUTER_DIAMETER,
                    h=(
                        self.depth
                        + MOUNTING_TUBE_PROTRUSION
                        - self.front_depth
                    ),
                    anchor=Anchor.BOTTOM,
                ).at(
                    x,
                    y,
                    self.front_depth,
                    anchor=Anchor.BOTTOM,
                )

        reinforcement_positions = (
            (-self.mount_x, -self.mount_y + REINFORCEMENT_OFFSET),
            (self.mount_x, -self.mount_y + REINFORCEMENT_OFFSET),
            (-self.mount_x, REINFORCEMENT_OFFSET),
            (self.mount_x, -REINFORCEMENT_OFFSET),
            (-self.mount_x, self.mount_y - REINFORCEMENT_OFFSET),
            (self.mount_x, self.mount_y - REINFORCEMENT_OFFSET),
        )
        reinforcement_depth = (
            REINFORCEMENT_RECESS_DEPTH + REINFORCEMENT_HOLE_DEPTH
        )
        for x, y in reinforcement_positions:
            body = body + Cylinder(
                d=REINFORCEMENT_OUTER_DIAMETER,
                h=reinforcement_depth,
                anchor=Anchor.BOTTOM,
            ).at(
                x,
                y,
                self.depth - reinforcement_depth,
                anchor=Anchor.BOTTOM,
            )
            body = body + Hole(
                d=REINFORCEMENT_RECESS_DIAMETER,
                depth=REINFORCEMENT_RECESS_DEPTH,
                direction=(0, 0, -1),
            ).at(x, y, self.depth)
            body = body + Hole(
                d=REINFORCEMENT_HOLE_DIAMETER,
                depth=REINFORCEMENT_HOLE_DEPTH,
                direction=(0, 0, -1),
            ).at(x, y, self.depth - REINFORCEMENT_RECESS_DEPTH)

        for x, y in (
            (-LOCATOR_PIN_X, LOCATOR_PIN_Y),
            (LOCATOR_PIN_X, -LOCATOR_PIN_Y),
        ):
            body = body + Cylinder(
                d=LOCATOR_PIN_DIAMETER,
                h=LOCATOR_PIN_PROTRUSION,
                anchor=Anchor.BOTTOM,
            ).at(
                x,
                y,
                self.depth,
                anchor=Anchor.BOTTOM,
            )

        rear_bore_start = self.depth + MOUNTING_TUBE_PROTRUSION
        rear_bore_depth = rear_bore_start - self.front_depth
        for x in (-self.mount_x, self.mount_x):
            for y in (-self.mount_y, 0, self.mount_y):
                body = body + Hole(
                    d=self.hole_diameter,
                    depth=rear_bore_depth,
                    direction=(0, 0, -1),
                ).at(x, y, rear_bore_start)

        return body


class ComponentCylinderOccurrence:
    def build(self):
        center_z = 160.0
        central = Hub75HistoryPanel(
            placement=Placement(
                z=center_z,
                rotation=(X, 90),
            )
        )
        assembly = central

        for index in (0, 1, 3, 4):
            x = (index - 2) * 160.0
            rotation = (
                ((0, 1, -1), 180)
                if index in (1, 3)
                else (X, 90)
            )
            assembly = assembly + central.copy(
                placement=Placement(
                    x=x,
                    z=center_z,
                    rotation=rotation,
                )
            )

        return assembly


ComponentCylinderOccurrence()
