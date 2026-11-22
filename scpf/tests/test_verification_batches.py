"""Guard Forge-owned runtime batching and generic output projection."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
CAD_CI = ROOT / "cad-ci.yml"
MODEL_BATCH_CI = ROOT / "ci" / "model-verification-batch" / "ci.yml"
REFERENCE_BATCH_CI = ROOT / "ci" / "reference-verification-batch" / "ci.yml"
DIAGRAM_CI = ROOT / "ci" / "verification-diagrams" / "ci.yml"
MODEL_BATCH = ROOT / "scripts" / "model_verification_batch.py"
REFERENCE_BATCH = ROOT / "scripts" / "reference_verification_batch.py"
REFERENCE_VALIDATION = ROOT / "verification" / "reference_validation.py"
BUILD123D_EXPORT = ROOT / "verification" / "build123d_export.py"


class VerificationBatchContractTests(unittest.TestCase):
    """Keep logical child items separate from expensive runtime startup."""

    def test_case_templates_use_generic_dependency_copy(self):
        text = CAD_CI.read_text(encoding="utf-8")
        self.assertIn("- model-verification-batch", text)
        self.assertIn("- reference-verification-batch", text)
        self.assertEqual(text.count("copy:"), 3)
        self.assertIn("dependency: model-verification-batch", text)
        self.assertEqual(
            text.count("dependency: reference-verification-batch"),
            2,
        )
        self.assertEqual(text.count("source: items/{item_path}"), 3)
        self.assertNotIn("materialize]", text)

    def test_no_model_item_overrides_copy_with_materializer(self):
        for path in sorted((ROOT / "examples").glob("*/ci.yml")):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn(
                "model_verification_batch.py, materialize",
                text,
                path.as_posix(),
            )

    def test_batch_items_publish_item_projection_roots(self):
        model = MODEL_BATCH_CI.read_text(encoding="utf-8")
        reference = REFERENCE_BATCH_CI.read_text(encoding="utf-8")
        self.assertIn("- items", model)
        self.assertNotIn("- models", model)
        self.assertIn("- items", reference)
        self.assertIn("- diagrams", reference)
        self.assertNotIn("- references", reference)

    def test_reference_batch_groups_all_four_engines(self):
        text = REFERENCE_VALIDATION.read_text(encoding="utf-8")
        self.assertIn(
            'IMPLEMENTATIONS = ("pythonscad", "pybosl2", "cadquery", "build123d")',
            text,
        )
        self.assertIn("for implementation in implementations:", text)
        self.assertIn("for slug in slugs:", text)
        self.assertIn("export_build123d_batch", text)

    def test_build123d_batch_imports_once_and_continues_cases(self):
        text = BUILD123D_EXPORT.read_text(encoding="utf-8")
        self.assertEqual(text.count("from build123d import export_stl"), 1)
        self.assertIn("for row in rows:", text)
        self.assertIn("continue so every case gets a result", text)
        self.assertIn("return 1 if failed else 0", text)

    def test_model_batch_writes_selected_child_owned_paths_directly(self):
        text = MODEL_BATCH.read_text(encoding="utf-8")
        ci_text = MODEL_BATCH_CI.read_text(encoding="utf-8")
        self.assertIn("selection_context: direct_dependents", ci_text)
        self.assertIn("def active_declarative_slugs(", text)
        self.assertIn('os.environ.get("CAD_CI_ACTIVE_DEPENDENTS_JSON")', text)
        self.assertIn("for slug in slugs:", text)
        self.assertIn(
            'case_root = batch_root / "examples" / slug',
            text,
        )
        self.assertIn(
            '"output": f"/output/items/examples/{slug}/model_verify"',
            text,
        )
        self.assertIn("for row in rows:", text)
        self.assertNotIn("materialize_case", text)
        self.assertNotIn("dependency_output_root", text)

    def test_reference_batch_builds_child_projection_once(self):
        text = REFERENCE_BATCH.read_text(encoding="utf-8")
        self.assertEqual(text.count('"docker",\n            "run"'), 1)
        self.assertIn("/workspace/scripts/build_diagrams.py", text)
        self.assertIn("/output/diagrams", text)
        self.assertIn("def build_item_projections(", text)
        self.assertIn('/ "examples"\n                / slug', text)
        self.assertIn('/ implementation\n                / "references"', text)
        self.assertIn('"implementations": [implementation_row]', text)
        self.assertIn('Path("/output") / name', text)
        self.assertIn('for name in ("references", "diagrams")', text)
        self.assertNotIn('shutil.rmtree(output / "references")', text)
        self.assertNotIn("materialize_case", text)
        self.assertNotIn("materialize_diagrams", text)
        self.assertNotIn("dependency_output_root", text)

    def test_diagram_item_uses_generic_copy(self):
        text = DIAGRAM_CI.read_text(encoding="utf-8")
        self.assertIn("copy:", text)
        self.assertIn("dependency: reference-verification-batch", text)
        self.assertIn("source: .", text)
        self.assertNotIn("run:", text)


if __name__ == "__main__":
    unittest.main()
