"""Native verification for #753 component-local Cylinder occurrence fixture."""

from cad_verification import (
    BodyEnvelope,
    SolidCraftModelExpectation,
    SolidCraftVerification,
)


VERIFICATION = SolidCraftVerification(
    verification_id="component-cylinder-occurrence",
    baseline=SolidCraftModelExpectation(
        body_envelopes=(
            BodyEnvelope((-40.0, -5.5, -5.0), (-20.0, 2.0, 5.0)),
            BodyEnvelope((20.0, -5.5, -5.0), (40.0, 2.0, 5.0)),
        ),
        bounds_tolerance=0.001,
    ),
)
