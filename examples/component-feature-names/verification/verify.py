"""Native SolidCraft verification for #679 feature-name namespaces."""

from cad_verification import (
    SolidCraftModelExpectation,
    SolidCraftTimelineExpectation,
    SolidCraftVerification,
)


VERIFICATION = SolidCraftVerification(
    verification_id="component-feature-names",
    baseline=SolidCraftModelExpectation(
        body_count=4,
        sketch_count=4,
        timeline=(
            SolidCraftTimelineExpectation(
                "Sketch",
                name="d1_LeftPanel_Profile",
                check_name=True,
                check_error=False,
                check_warning=False,
            ),
            SolidCraftTimelineExpectation(
                "Sketch",
                name="d2_RightPanel_Profile",
                check_name=True,
                check_error=False,
                check_warning=False,
            ),
            SolidCraftTimelineExpectation(
                "Sketch",
                name="d3_Strip_Profile",
                check_name=True,
                check_error=False,
                check_warning=False,
            ),
            SolidCraftTimelineExpectation(
                "Sketch",
                name="d4_Strip_2_Profile",
                check_name=True,
                check_error=False,
                check_warning=False,
            ),
        ),
    ),
)
