"""Native regression fixture for component-local Cylinder join placement."""


class BossedPanel:
    def build(self):
        body = Box(20, 10, 4)

        # Deliberately overlap the plate by 0.5 mm so SolidCraft performs one
        # unambiguous native join. The boss protrudes far enough to make stale
        # source/tool geometry visually obvious in the presentation preview.
        boss = Cylinder(
            d=4,
            h=4,
            anchor=Anchor.BOTTOM,
        ).at(
            6,
            0,
            1.5,
            anchor=Anchor.BOTTOM,
        )
        return body + boss


class ComponentCylinderOccurrence:
    def build(self):
        left = BossedPanel(
            placement=Placement(
                x=-30,
                rotation=(X, 90),
            )
        )
        right = left.copy(
            placement=Placement(
                x=30,
                rotation=(X, 90),
            )
        )
        return left + right


ComponentCylinderOccurrence()
