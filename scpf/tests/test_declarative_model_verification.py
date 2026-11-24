"""Guard the complete declarative model-verification boundary."""

from __future__ import annotations

from pathlib import Path
import unittest

from repository_fixtures import FIXTURE_ROOTS, fixture_root


ROOT = Path(__file__).resolve().parents[2]
LAUNCHER = ROOT / "scripts" / "model_verify_declarative.py"
BATCH = ROOT / "scripts" / "model_verification_batch.py"

BATCH_ONE_MODELS = (
    "anchored-holes",
    "hole-family",
    "sheet-fold",
    "top-sketch-after-chamfer",
    "parameter-scope",
    "parent-derived-child-size",
    "components",
    "repeated-parent-attachments",
    "assembly-decorator",
    "group-hierarchy",
)

BATCH_ONE_SAVED_DESIGN_MODELS = {
    "parameter-scope",
    "parent-derived-child-size",
    "repeated-parent-attachments",
}

BATCH_TWO_MODELS = (
    "bracket",
    "circle-negative-extrude",
    "circular-feature-pattern",
    "eight-flightcase-corners",
    "primitive-csg",
    "rectangular-pattern",
    "round-top-sketch",
    "rounded-rectangle-sketch",
    "selective-profile-extrude",
    "slot-family",
)

BATCH_TWO_SAVED_DESIGN_MODELS = {
    "circular-feature-pattern",
    "eight-flightcase-corners",
    "rectangular-pattern",
    "selective-profile-extrude",
    "slot-family",
}

MIGRATED_MODELS = (
    "simple-box",
    "anchor-topology-mutation",
    "assembly-owned-anchor",
    "attach-angle",
    "corner-anchor",
    "eight-corner-brackets",
    "four-corner-l",
    "parametric-anchor",
    "parametric-attach",
    "parametric-offset",
    "xz-anchor",
    *BATCH_ONE_MODELS,
    *BATCH_TWO_MODELS,
    "sketch-pattern-mirror",
)

ACTIVATED_FINAL_SIX = (
    "assembly-owned-anchor",
    "corner-anchor",
    "eight-corner-brackets",
    "parametric-anchor",
    "parametric-attach",
    "parametric-offset",
)

FORBIDDEN_VERIFY_IMPLEMENTATION = (
    "argparse",
    "run_command",
    "run_document",
    "VerificationCheck",
    "VerificationContext",
    "solidcraft-cli",
    "model.yml",
    "import yaml",
)


class DeclarativeModelVerificationBoundaryTests(unittest.TestCase):
    """Keep Forge as producer/data owner rather than CAD checker owner."""

    def test_migrated_models_use_verify_data_only(self):
        """Every migrated model uses verify.py and the shared launcher."""

        for slug in MIGRATED_MODELS:
            with self.subTest(slug=slug):
                verification = fixture_root(slug) / "verification"
                self.assertTrue((verification / "verify.py").is_file())
                self.assertFalse((verification / "verify_model.py").exists())

                ci = (
                    fixture_root(slug) / "ci.yml"
                ).read_text(encoding="utf-8")
                self.assertIn("template: forge-model-declarative", ci)
                self.assertNotIn("steps:", ci)
                root_ci = (ROOT / "cad-ci.yml").read_text(encoding="utf-8")
                builder = (
                    ROOT
                    / "ci"
                    / "builders"
                    / "model-verification-batch"
                    / "builder.yml"
                ).read_text(encoding="utf-8")
                self.assertIn("builder: forge-model", root_ci)
                self.assertIn(
                    "scripts/model_verification_batch.py",
                    builder,
                )
                self.assertNotIn("scripts/model_verify.py", builder)

                text = (verification / "verify.py").read_text(
                    encoding="utf-8"
                )
                for value in FORBIDDEN_VERIFY_IMPLEMENTATION:
                    self.assertNotIn(value, text)

    def test_batch_one_saved_design_contract_is_model_specific(self):
        """Only the three historical batch-one mutation cases keep mutations."""

        for slug in BATCH_ONE_MODELS:
            with self.subTest(slug=slug):
                text = (
                    fixture_root(slug) / "verification" / "verify.py"
                ).read_text(encoding="utf-8")
                has_saved_design = "SolidCraftSavedDesign(" in text
                self.assertEqual(
                    has_saved_design,
                    slug in BATCH_ONE_SAVED_DESIGN_MODELS,
                )

    def test_batch_two_saved_design_contract_is_model_specific(self):
        """Keep the explicit batch-two saved-design coverage list authoritative."""

        for slug in BATCH_TWO_MODELS:
            with self.subTest(slug=slug):
                text = (
                    ROOT / "examples" / slug / "verification" / "verify.py"
                ).read_text(encoding="utf-8")
                has_saved_design = "SolidCraftSavedDesign(" in text
                self.assertEqual(
                    has_saved_design,
                    slug in BATCH_TWO_SAVED_DESIGN_MODELS,
                )

    def test_simple_box_keeps_its_model_specific_mutation(self):
        """The representative model keeps its own mutation command data."""

        verification = fixture_root("simple-box") / "verification"
        self.assertTrue((verification / "change_length.json").is_file())

    def test_reference_qualification_set_has_no_procedural_verifiers(self):
        """The historical reference-qualified set stays declarative after moves."""

        self.assertEqual(len(MIGRATED_MODELS), 32)
        procedural = [
            path
            for root in FIXTURE_ROOTS
            for path in root.glob("*/verification/verify_model.py")
        ]
        self.assertEqual(procedural, [])

    def test_all_qualification_models_are_processed_with_references(self):
        """All 32 declarative cases are active with four reference children."""

        for slug in MIGRATED_MODELS:
            with self.subTest(slug=slug):
                ci = (
                    fixture_root(slug) / "ci.yml"
                ).read_text(encoding="utf-8")
                self.assertIn("process: true", ci)

                for engine in (
                    "build123d",
                    "cadquery",
                    "pybosl2",
                    "pythonscad",
                ):
                    child = fixture_root(slug) / engine / "ci.yml"
                    self.assertTrue(
                        child.is_file(),
                        f"missing reference child: {child}",
                    )

    def test_final_six_use_standard_model_template(self):
        """The six newly activated cases use the standard declarative template."""

        for slug in ACTIVATED_FINAL_SIX:
            with self.subTest(slug=slug):
                ci = (
                    fixture_root(slug) / "ci.yml"
                ).read_text(encoding="utf-8")
                self.assertIn("template: forge-model-declarative", ci)

    def test_batch_reuses_runtime_and_emits_child_projection_roots(self):
        text = BATCH.read_text(encoding="utf-8")
        self.assertIn("processed_declarative_slugs", text)
        self.assertIn('"docker"', text)
        self.assertIn('"run"', text)
        self.assertIn("for row in rows:", text)
        self.assertIn("for slug, source_path in items:", text)
        self.assertIn("case_root = batch_root / source_path", text)
        self.assertIn(
            'f"/output/items/{source_path}/model_verify"',
            text,
        )
        self.assertNotIn("dependency_output_root", text)
        self.assertNotIn("materialize_case", text)

    def test_shared_launcher_supports_narrow_sketch_only_production(self):
        """Sketch-only replay skips only body-dependent producer artifacts."""

        text = LAUNCHER.read_text(encoding="utf-8")
        self.assertIn("def _is_sketch_only_document", text)
        self.assertIn('command == "parameters.add"', text)
        self.assertIn('command.startswith("sketch.")', text)
        self.assertIn(
            'export=None if sketch_only else native / "model.step"',
            text,
        )
        self.assertIn("if not sketch_only:", text)

    def test_shared_launcher_only_produces_and_hands_off(self):
        """Forge launcher may replay Forge output but not check SolidCraft data."""

        text = LAUNCHER.read_text(encoding="utf-8")
        self.assertIn("run_document", text)
        self.assertIn("run_solidcraft_verification", text)

        forbidden_checker_knowledge = (
            '"solidcraft-cli"',
            "'solidcraft-cli'",
            '"body_count"',
            "'body_count'",
            '"bbox"',
            "'bbox'",
            '"timeline"',
            "'timeline'",
            '"params"',
            "'params'",
        )
        for value in forbidden_checker_knowledge:
            with self.subTest(value=value):
                self.assertNotIn(value, text)


if __name__ == "__main__":
    unittest.main()
