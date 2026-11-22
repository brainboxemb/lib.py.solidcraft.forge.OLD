"""Native saved-design verification for the #567 connected-profile fixture."""

from __future__ import annotations

from pathlib import Path

from cad_verification import (
    BodyEnvelope,
    SolidCraftBodyExpectation,
    SolidCraftModelExpectation,
    SolidCraftSavedDesign,
    SolidCraftSketchExpectation,
    SolidCraftTimelineExpectation,
    SolidCraftVerification,
)


HERE = Path(__file__).resolve().parent


COMMON_BODY = SolidCraftBodyExpectation(
    sheet_metal=True,
    closed=True,
)

COMMON_SKETCH = SolidCraftSketchExpectation(
    name="Connected blank",
    profiles=1,
    curves=4,
    status="solved",
)


VERIFICATION = SolidCraftVerification(
    verification_id="connected-profile-sheet",
    baseline=SolidCraftModelExpectation(
        body_count=1,
        body_envelopes=(
            BodyEnvelope((-60.0, -20.0, 0.0), (60.0, 20.0, 2.0)),
        ),
        bounds_tolerance=0.01,
        parameters={
            "half_span": 40.0,
            "radius": 20.0,
            "thickness": 2.0,
            "bend_radius": 2.0,
            "k_factor": 0.5,
        },
        parameter_match="subset",
        named_bodies=(COMMON_BODY,),
        sketch_count=1,
        sketches=(COMMON_SKETCH,),
        timeline=(
            SolidCraftTimelineExpectation(
                "Sketch",
                name="Connected blank",
                check_name=True,
                check_error=False,
                check_warning=False,
            ),
            SolidCraftTimelineExpectation(
                "BaseFlangeFeature",
                name="BaseFlange1",
                check_name=True,
                check_error=False,
                check_warning=False,
            ),
        ),
    ),
    saved_designs=(
        SolidCraftSavedDesign(
            id="resize_connected_profile",
            command_path=HERE / "change_geometry.json",
            expectation=SolidCraftModelExpectation(
                body_count=1,
                body_envelopes=(
                    BodyEnvelope((-75.0, -25.0, 0.0), (75.0, 25.0, 2.0)),
                ),
                bounds_tolerance=0.01,
                parameters={
                    "half_span": 50.0,
                    "radius": 25.0,
                },
                parameter_match="subset",
                named_bodies=(COMMON_BODY,),
                sketch_count=1,
                sketches=(COMMON_SKETCH,),
            ),
        ),
    ),
)
