"""Saved-design verification for the #683 open connected Sketch-chain fixture."""

from __future__ import annotations

from pathlib import Path

from cad_verification import (
    SolidCraftModelExpectation,
    SolidCraftSavedDesign,
    SolidCraftSketchExpectation,
    SolidCraftTimelineExpectation,
    SolidCraftVerification,
)


HERE = Path(__file__).resolve().parent


COMMON_SKETCH = SolidCraftSketchExpectation(
    name="Contour Path",
    profiles=0,
    curves=3,
)


VERIFICATION = SolidCraftVerification(
    verification_id="open-sketch-chain",
    baseline=SolidCraftModelExpectation(
        body_count=0,
        parameters={
            "length": 40.0,
            "end_height": 30.0,
        },
        parameter_match="subset",
        sketch_count=1,
        sketches=(COMMON_SKETCH,),
        timeline=(
            SolidCraftTimelineExpectation(
                "Sketch",
                name="Contour Path",
                check_name=True,
                check_error=False,
                check_warning=False,
            ),
        ),
    ),
    saved_designs=(
        SolidCraftSavedDesign(
            id="resize_open_chain",
            command_path=HERE / "change_geometry.json",
            expectation=SolidCraftModelExpectation(
                body_count=0,
                parameters={
                    "length": 45.0,
                    "end_height": 35.0,
                },
                parameter_match="subset",
                sketch_count=1,
                sketches=(COMMON_SKETCH,),
            ),
        ),
    ),
)
