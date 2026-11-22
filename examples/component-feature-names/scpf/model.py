"""Regression fixture for component-local native feature-name namespaces."""


@component
class LeftPanel:
    def build(self):
        with Sketch(name="Profile", plane="XY") as sketch:
            Rectangle2D(20, 10)
        return sketch.extrude(4)


@component
class RightPanel:
    def build(self):
        with Sketch(name="Profile", plane="XY") as sketch:
            Rectangle2D(24, 12)
        return sketch.extrude(5)


@component
class Strip:
    width = 10.0

    def build(self):
        with Sketch(name="Profile", plane="XY") as sketch:
            Rectangle2D(self.width, 8)
        return sketch.extrude(3)


class FeatureNameAssembly:
    def build(self):
        left = LeftPanel()
        right = RightPanel(placement=Placement(x=40))
        narrow = Strip(width=10, placement=Placement(x=80))
        wide = Strip(width=14, placement=Placement(x=110))
        return left + right + narrow + wide


FeatureNameAssembly()
