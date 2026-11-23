"""Native regression fixture for component-local Sketch feature names."""


class LeftPlate:
    def build(self):
        with Sketch(name="Profile", plane="XY") as sketch:
            Rectangle2D(20, 16)
        return sketch.extrude(4)


class RightPlate:
    def build(self):
        with Sketch(name="Profile", plane="XY") as sketch:
            Rectangle2D(30, 18)
        return sketch.extrude(6)


class ReusedLocalNames:
    def build(self):
        left = LeftPlate(
            placement=Placement(x=-30),
        )
        right = RightPlate(
            placement=Placement(x=30),
        )
        return left + right


ReusedLocalNames()
