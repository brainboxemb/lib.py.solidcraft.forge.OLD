"""Keep Forge runtime/workflow consumption explicit and externally owned."""

from pathlib import Path
import re
import unittest

from scpf.version import TESTED_SOLIDCRAFT_VERSION


ROOT = Path(__file__).resolve().parents[2]
CAD_CI = ROOT / "cad-ci.yml"
WORKFLOW = ROOT / ".github" / "workflows" / "scpf.yml"
MODEL_VERIFY = ROOT / "scripts" / "model_verify_declarative.py"
MODEL_BATCH = ROOT / "scripts" / "model_verification_batch.py"
REFERENCE_BATCH = ROOT / "scripts" / "reference_verification_batch.py"
TOOL_RELEASE = "v0.35.0"


def configured_variable(name: str) -> str:
    """Read one quoted or plain root CAD-CI variable without YAML."""

    text = CAD_CI.read_text(encoding="utf-8")
    match = re.search(
        rf"^  {re.escape(name)}:\s*[\"']?([^\"'\s]+)[\"']?\s*$",
        text,
        re.MULTILINE,
    )
    if match is None:
        raise AssertionError(f"missing CAD-CI variable: {name}")
    return match.group(1)


class CiRuntimeContractTests(unittest.TestCase):
    """Prove Forge consumes released owner runtime/workflow contracts."""

    def test_runtime_roles_use_owner_candidate_edge_for_qualification(self):
        solidcraft = configured_variable("FORGE_RUNTIME_IMAGE")
        reference = configured_variable("REFERENCE_RUNTIME_IMAGE")
        self.assertEqual(
            solidcraft,
            "ghcr.io/brainboxemb/cad-solidcraft:edge",
        )
        self.assertEqual(
            reference,
            "ghcr.io/brainboxemb/cad-reference:edge",
        )
        config = CAD_CI.read_text(encoding="utf-8")
        self.assertIn(
            'reference: "ghcr.io/brainboxemb/cad-reference:edge"',
            config,
        )
        self.assertNotIn(":v0.3.5", config)

    def test_forge_owned_runtime_consumers_keep_separate_roles(self):
        model_text = MODEL_BATCH.read_text(encoding="utf-8")
        reference_text = REFERENCE_BATCH.read_text(encoding="utf-8")
        self.assertIn('os.environ.get("FORGE_RUNTIME_IMAGE"', model_text)
        self.assertNotIn("REFERENCE_RUNTIME_IMAGE", model_text)
        self.assertIn('os.environ.get("REFERENCE_RUNTIME_IMAGE"', reference_text)
        self.assertNotIn('os.environ.get("FORGE_RUNTIME_IMAGE"', reference_text)

    def test_builtin_reference_engines_are_not_in_forge_runtime_batch(self):
        config = CAD_CI.read_text(encoding="utf-8")
        reference_text = REFERENCE_BATCH.read_text(encoding="utf-8")
        validation = (
            ROOT / "verification" / "reference_validation.py"
        ).read_text(encoding="utf-8")

        self.assertIn("builder: cadquery", config)
        self.assertIn("builder: build123d", config)
        self.assertIn("adapter: mesh-geometry", config)
        self.assertIn(
            'IMPLEMENTATIONS = ("pythonscad", "pybosl2")',
            reference_text,
        )
        self.assertIn(
            'IMPLEMENTATIONS = ("pythonscad", "pybosl2")',
            validation,
        )
        self.assertNotIn("export_build123d", validation)
        self.assertFalse(
            (ROOT / "verification" / "build123d_export.py").exists()
        )

    def test_model_launcher_exposes_cold_path_timing(self):
        text = MODEL_VERIFY.read_text(encoding="utf-8")
        for label in (
            "compile_commands_s=",
            "image_pull_s=",
            "container_start_s=",
            "python_bootstrap_s=",
            "cad_verification_import_s=",
            "definition_load_s=",
            "native_model_s=",
            "solidcraft_verification_s=",
            "inside_runtime_total_s=",
            "container_process_total_s=",
        ):
            self.assertIn(label, text)
        self.assertIn("time.perf_counter()", text)

    def test_forge_owned_batches_start_one_container_per_batch(self):
        model_text = MODEL_BATCH.read_text(encoding="utf-8")
        reference_text = REFERENCE_BATCH.read_text(encoding="utf-8")

        self.assertEqual(model_text.count('"docker",\n            "run"'), 1)
        self.assertEqual(reference_text.count('"docker",\n            "run"'), 1)
        self.assertIn("for row in rows:", model_text)
        self.assertIn("processed_reference_slugs", reference_text)

    def test_solidcraft_version_matches_forge(self):
        self.assertEqual(
            configured_variable("SOLIDCRAFT_VERSION"),
            TESTED_SOLIDCRAFT_VERSION,
        )

    def test_forge_owns_no_runtime_or_verification_packaging(self):
        self.assertFalse((ROOT / "docker" / "solidcraft_runtime").exists())
        self.assertFalse(
            (ROOT / ".github" / "workflows" / "solidcraft-runtime.yml").exists()
        )
        self.assertFalse((ROOT / "scripts" / "solidcraft_runtime.py").exists())
        self.assertFalse((ROOT / "scripts" / "verification_package.py").exists())
        self.assertFalse((ROOT / "ci" / "cad-verification-package").exists())

    def test_normal_workflow_delegates_to_released_cad_ci(self):
        text = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn("types: [opened, synchronize, reopened]", text)
        self.assertIn("branches: [main, dev-cad, dev-ci]", text)
        self.assertIn("workflow_dispatch:", text)
        self.assertIn("# template-version: 5", text)
        self.assertIn("item: ${{ inputs.item }}", text)
        self.assertIn("changed_paths: ${{ inputs.changed_paths }}", text)
        self.assertIn(
            f"reusable-ci.yml@{TOOL_RELEASE}",
            text,
        )
        self.assertIn(
            f"reusable-durable.yml@{TOOL_RELEASE}",
            text,
        )
        self.assertEqual(text.count("jobs: 2"), 3)
        self.assertIn('"stable_branch":"main"', text)
        self.assertIn(
            '"development_branches":["dev-cad","dev-ci"]',
            text,
        )
        self.assertIn('"docs_only_prefixes":["docs/"]', text)
        self.assertIn("source_sha: ${{ github.sha }}", text)
        self.assertIn("source_ref: ${{ github.ref_name }}", text)
        self.assertIn("scope: ${{ github.ref_name }}", text)
        self.assertIn("build_branch: build", text)
        self.assertIn("pages_branch: gh-pages", text)

        for forbidden in (
            "brainboxemb/tool.cad.ci@",
            "runs-on: ubuntu-latest",
            "gh api",
            "/pulls/",
            "files?per_page",
            "Classify pull request",
            "actions/checkout",
            "actions/setup-python",
            "pip install",
            "publish build",
            "publish pages",
            "PREPARED_SCOPE",
            "BUILD_COMMIT",
            "actions/upload-artifact",
            "actions/download-artifact",
        ):
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
