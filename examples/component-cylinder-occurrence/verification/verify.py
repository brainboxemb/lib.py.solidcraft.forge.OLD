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
            BodyEnvelope((-399.85, -17.5, 0.145), (-240.15, 0.0, 319.855)),
            BodyEnvelope((-239.85, -17.5, 0.145), (-80.15, 0.0, 319.855)),
            BodyEnvelope((-79.85, -17.5, 0.145), (79.85, 0.0, 319.855)),
            BodyEnvelope((80.15, -17.5, 0.145), (239.85, 0.0, 319.855)),
            BodyEnvelope((240.15, -17.5, 0.145), (399.85, 0.0, 319.855)),
        ),
        bounds_tolerance=0.01,
    ),
)
