"""SolidCraft regression fixture for reusable open connected Sketch chains."""


class OpenSketchChain:
    length = 40.0
    end_height = 30.0

    def build(self):
        with Sketch(name="Contour Path", plane="XY") as sketch:
            chain = sketch.chain(start=(0, 0))
            chain.line_to((self.length, 0))
            chain.tangent_arc_to((50, 10))
            chain.line_to((50, self.end_height))
            path = chain.finish()

        return path


OpenSketchChain()
