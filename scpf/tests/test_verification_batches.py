"""Guard Forge-owned batches and generic built-in reference ownership."""

from pathlib import Path
import unittest

from repository_fixtures import FIXTURE_ROOTS


ROOT = Path(__file__).resolve().parents[2]
CAD_CI = ROOT / "cad-ci.yml"
MODEL_BATCH_CI = ROOT / "ci" / "model-verification-batch" / "ci.yml"
REFERENCE_BATCH_CI = ROOT / "ci" / "reference-verification-batch" / "ci.yml"
DIAGRAM_CI = ROOT / "ci" / "verification-diagrams" / "ci.yml"
BUILDERS = ROOT / "ci" / "builders"
MODEL_BATCH = ROOT / "scripts" / "model_verification_batch.py"
REFERENCE_BATCH = ROOT / "scripts" / "reference_verification_batch.py"
REFERENCE_VALIDATION = ROOT / "verification" / "reference_validation.py"


class VerificationBatchContractTests(unittest.TestCase):
    """Keep expensive Forge work separate from generic built-in execution."""

    def test_model_template_projects_through_repository_builder(self):
        config = CAD_CI.read_text(encoding="utf-8")
        builder = (
            BUILDERS / "forge-model" / "builder.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("builder: forge-model", config)
        self.assertIn("dependency: model-verification-batch", builder)
        self.assertIn("source: items/{item_path}", builder)
        self.assertNotIn("copy:", config)

    def test_reference_templates_split_generic_and_forge_owners(self):
        config = CAD_CI.read_text(encoding="utf-8")
        projection = (
            BUILDERS / "forge-reference-projection" / "builder.yml"
        ).read_text(encoding="utf-8")

        self.assertIn("builder: forge-reference-projection", config)
        self.assertIn("dependency: reference-verification-batch", projection)
        self.assertIn("source: items/{item_path}", projection)
        self.assertIn("builder: cadquery", config)
        self.assertIn("builder: build123d", config)
        self.assertEqual(config.count("adapter: mesh-geometry"), 2)

    def test_normal_item_configs_have_no_execution_plumbing(self):
        for root in FIXTURE_ROOTS:
            for pattern in ("*/ci.yml", "*/*/ci.yml"):
                for path in sorted(root.glob(pattern)):
                    text = path.read_text(encoding="utf-8")
                    self.assertNotIn("steps:", text, path.as_posix())
                    self.assertNotIn("run:", text, path.as_posix())
                    self.assertNotIn("copy:", text, path.as_posix())

    def test_batch_items_select_repository_builders(self):
        model = MODEL_BATCH_CI.read_text(encoding="utf-8")
        reference = REFERENCE_BATCH_CI.read_text(encoding="utf-8")
        self.assertIn("builder: model-verification-batch", model)
        self.assertIn("builder: reference-verification-batch", reference)
        self.assertNotIn("steps:", model)
        self.assertNotIn("steps:", reference)

    def test_model_batch_keeps_active_direct_dependent_context(self):
        builder = (
            BUILDERS / "model-verification-batch" / "builder.yml"
        ).read_text(encoding="utf-8")
        text = MODEL_BATCH.read_text(encoding="utf-8")
        self.assertIn("selection_context: direct_dependents", builder)
        self.assertIn("def active_declarative_items(", text)
        self.assertIn('os.environ.get("CAD_CI_ACTIVE_DEPENDENTS_JSON")', text)
        self.assertIn("for slug, source_path in items:", text)
        self.assertIn(
            'f"/output/items/{source_path}/model_verify"',
            text,
        )
        self.assertNotIn("materialize_case", text)
        self.assertNotIn("dependency_output_root", text)

    def test_forge_reference_batch_owns_only_pythonscad_and_pybosl2(self):
        batch = REFERENCE_BATCH.read_text(encoding="utf-8")
        validation = REFERENCE_VALIDATION.read_text(encoding="utf-8")
        builder = (
            BUILDERS / "reference-verification-batch" / "builder.yml"
        ).read_text(encoding="utf-8")

        self.assertIn(
            'IMPLEMENTATIONS = ("pythonscad", "pybosl2")',
            batch,
        )
        self.assertIn(
            'IMPLEMENTATIONS = ("pythonscad", "pybosl2")',
            validation,
        )
        self.assertNotIn("examples/*/build123d/**", builder)
        self.assertNotIn("examples/*/cadquery/**", builder)
        self.assertIn("verification/cases/*/pythonscad/**", builder)
        self.assertIn("verification/cases/*/pybosl2/**", builder)
        self.assertIn("def processed_reference_items(", batch)
        self.assertIn(
            "for slug, source_path in items_by_slug.items():",
            batch,
        )
        self.assertIn(
            '/ source_path\n                / implementation',
            batch,
        )
        self.assertNotIn("export_build123d", validation)
        self.assertFalse(
            (ROOT / "verification" / "build123d_export.py").exists()
        )

    def test_reference_batch_builds_remaining_child_projections_once(self):
        text = REFERENCE_BATCH.read_text(encoding="utf-8")
        self.assertEqual(text.count('"docker",\n            "run"'), 1)
        self.assertIn("/workspace/scripts/build_diagrams.py", text)
        self.assertIn("/output/diagrams", text)
        self.assertIn("def build_item_projections(", text)
        self.assertIn('/ implementation\n                / "references"', text)
        self.assertIn('"implementations": [implementation_row]', text)
        self.assertNotIn("materialize_case", text)
        self.assertNotIn("dependency_output_root", text)

    def test_diagram_item_uses_repository_copy_builder(self):
        item = DIAGRAM_CI.read_text(encoding="utf-8")
        builder = (
            BUILDERS / "verification-diagrams" / "builder.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("builder: verification-diagrams", item)
        self.assertNotIn("steps:", item)
        self.assertIn("copy:", builder)
        self.assertIn("dependency: reference-verification-batch", builder)
        self.assertIn("source: .", builder)


if __name__ == "__main__":
    unittest.main()
