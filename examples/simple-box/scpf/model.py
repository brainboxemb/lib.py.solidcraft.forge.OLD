"""Smallest SCPF regression example: one parameterized, editable Box.

#661 selectivity probe: source-only comment; geometry and command contract are unchanged.
"""


class SimpleBox:
    length = 40.0
    width = 30.0
    height = 10.0

    def build(self):
        return Box(self.length, self.width, self.height, anchor=Anchor.BOTTOM)


SimpleBox()
