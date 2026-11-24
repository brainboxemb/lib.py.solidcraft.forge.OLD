"""Native verification for #753 HUB75-style component history."""

from cad_verification import (
    BodyEnvelope,
    SolidCraftModelExpectation,
    SolidCraftVerification,
)


VERIFICATION = SolidCraftVerification(
    verification_id="component-cylinder-occurrence",
    baseline=SolidCraftModelExpectation(
        body_envelopes=(
            BodyEnvelope((-399.85, -156.25, 0.145), (-240.15, 156.25, 319.855)),
            BodyEnvelope((-239.85, -156.25, 0.145), (-80.15, 156.25, 319.855)),
            BodyEnvelope((-79.85, -156.25, 0.145), (79.85, 156.25, 319.855)),
            BodyEnvelope((80.15, -156.25, 0.145), (239.85, 156.25, 319.855)),
            BodyEnvelope((240.15, -156.25, 0.145), (399.85, 156.25, 319.855)),
        ),
        bounds_tolerance=0.01,
    ),
)
