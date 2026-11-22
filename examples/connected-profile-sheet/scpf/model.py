"""Native regression fixture for connected mixed line/arc sheet profiles."""


class ConnectedProfileSheet:
    half_span = 40.0
    radius = 20.0
    thickness = 2.0
    bend_radius = 2.0
    k_factor = 0.5

    def build(self):
        with Sketch(name="Connected blank", plane="XY") as blank:
            contour = blank.profile(
                start=(-self.half_span, -self.radius),
            )
            contour.line_to((self.half_span, -self.radius))
            contour.arc_center_to(
                (self.half_span, self.radius),
                center=(self.half_span, 0),
            )
            contour.line_to((-self.half_span, self.radius))
            contour.arc_center_to(
                (-self.half_span, -self.radius),
                center=(-self.half_span, 0),
            )
            contour.close()

        return blank.sheet_metal(
            thickness=self.thickness,
            bend_radius=self.bend_radius,
            k_factor=self.k_factor,
            rule_name="Connected Profile Rule",
        )


ConnectedProfileSheet()
