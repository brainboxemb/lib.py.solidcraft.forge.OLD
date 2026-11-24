"""Native verification for the #679 component-local Sketch-name fixture."""

from cad_verification import (
    BodyEnvelope,
    SolidCraftModelExpectation,
    SolidCraftVerification,
)


VERIFICATION = SolidCraftVerification(
    verification_id="component-local-sketch-names",
    baseline=SolidCraftModelExpectation(
        body_envelopes=(
            BodyEnvelope((-40.0, -8.0, 0.0), (-20.0, 8.0, 4.0)),
            BodyEnvelope((15.0, -9.0, 0.0), (45.0, 9.0, 6.0)),
        ),
        bounds_tolerance=0.001,
    ),
)
