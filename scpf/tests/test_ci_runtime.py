"""Keep Forge runtime consumption explicit and externally owned."""

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
TOOL_COMMIT = "b62f9d0b169aa201a3c66c3166f364396b2d71bc"


def configured_variable(name: str) -> str:
    """Read one quoted or plain root CAD-CI variable without a YAML dependency."""

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
    """Prove Forge consumes the released external runtime roles."""

    def test_runtime_roles_are_external_immutable_releases(self):
        """Use matching SemVer role releases from docker.cad.solidcraft."""

        solidcraft = configured_variable("FORGE_RUNTIME_IMAGE")
        reference = configured_variable("REFERENCE_RUNTIME_IMAGE")
        self.assertRegex(
            solidcraft,
            r"^ghcr\.io/brainboxemb/cad-solidcraft:v\d+\.\d+\.\d+$",
        )
        self.assertRegex(
            reference,
            r"^ghcr\.io/brainboxemb/cad-reference:v\d+\.\d+\.\d+$",
        )
        self.assertEqual(
            solidcraft.rsplit(":", 1)[1],
            reference.rsplit(":", 1)[1],
        )
        self.assertEqual(solidcraft.rsplit(":", 1)[1], "v0.3.4")

    def test_runtime_consumers_use_separate_roles(self):
        """Keep model and reference execution on their own released images."""

        model_text = MODEL_BATCH.read_text(encoding="utf-8")
        reference_text = REFERENCE_BATCH.read_text(encoding="utf-8")
        self.assertIn('os.environ.get("FORGE_RUNTIME_IMAGE"', model_text)
        self.assertNotIn("REFERENCE_RUNTIME_IMAGE", model_text)
        self.assertIn('os.environ.get("REFERENCE_RUNTIME_IMAGE"', reference_text)
        self.assertNotIn('os.environ.get("FORGE_RUNTIME_IMAGE"', reference_text)

    def test_model_launcher_exposes_cold_path_timing(self):
        """Keep #484 timing decomposition visible without changing semantics."""

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

    def test_runtime_batches_start_one_container_per_batch(self):
        model_text = MODEL_BATCH.read_text(encoding="utf-8")
        reference_text = REFERENCE_BATCH.read_text(encoding="utf-8")

        self.assertEqual(model_text.count('"docker",\n            "run"'), 1)
        self.assertEqual(reference_text.count('"docker",\n            "run"'), 1)
        self.assertIn("for row in rows:", model_text)
        self.assertIn("processed_reference_slugs", reference_text)

    def test_solidcraft_version_matches_forge(self):
        """Keep Forge's compatibility declaration explicit."""

        self.assertEqual(
            configured_variable("SOLIDCRAFT_VERSION"),
            TESTED_SOLIDCRAFT_VERSION,
        )

    def test_forge_owns_no_runtime_packaging(self):
        """Runtime build and release files belong to docker.cad.solidcraft."""

        self.assertFalse((ROOT / "docker" / "solidcraft_runtime").exists())
        self.assertFalse(
            (ROOT / ".github" / "workflows" / "solidcraft-runtime.yml").exists()
        )
        self.assertFalse((ROOT / "scripts" / "solidcraft_runtime.py").exists())

    def test_normal_workflow_delegates_to_released_cad_ci(self):
        """Keep review policy and durable publication on released CAD-CI surfaces."""

        text = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn("types: [opened, synchronize, reopened]", text)
        self.assertIn("branches: [main, dev-cad, dev-ci]", text)
        self.assertIn("workflow_dispatch:", text)
        self.assertEqual(
            text.count(f"uses: brainboxemb/tool.cad.ci@{TOOL_COMMIT}"),
            2,
        )
        self.assertEqual(text.count('jobs: "2"'), 2)

        pr = text.split("  cad_ci_pr:", 1)[1].split(
            "  cad_ci_push:", 1
        )[0]
        self.assertIn("if: github.event_name == 'pull_request'", pr)
        self.assertIn("contents: read", pr)
        self.assertNotIn("contents: write", pr)
        self.assertIn("packages: read", pr)
        self.assertIn("pull-requests: read", pr)
        self.assertEqual(pr.count("runs-on: ubuntu-latest"), 1)
        self.assertIn(
            "Classify pull request before CAD CI bootstrap",
            pr,
        )
        self.assertIn("gh api --paginate", pr)
        self.assertIn("/pulls/${PR_NUMBER}/files?per_page=100", pr)
        self.assertIn('if [ "$BASE_REF" = "main" ]', pr)
        self.assertIn("docs/*", pr)
        self.assertIn("classification=docs-only", pr)
        self.assertIn("classification=cad-ci-required", pr)
        self.assertIn(
            "if: steps.classify.outputs.run_cad == 'false'",
            pr,
        )
        self.assertIn(
            "if: steps.classify.outputs.run_cad == 'true'",
            pr,
        )
        self.assertIn(
            "source_sha: ${{ github.event.pull_request.head.sha }}",
            pr,
        )
        self.assertIn(
            "base_sha: ${{ github.event.pull_request.base.sha }}",
            pr,
        )
        self.assertIn(
            "github.event.pull_request.head.ref == 'dev-cad'",
            pr,
        )
        self.assertIn(
            "github.event.pull_request.head.ref == 'dev-ci'",
            pr,
        )
        self.assertIn(
            "github.event.pull_request.head.ref == 'promote/dev-cad'",
            pr,
        )
        self.assertIn(
            "github.event.pull_request.head.ref == 'promote/dev-ci'",
            pr,
        )
        self.assertNotIn("durable_scope:", pr)
        self.assertNotIn("publish build", pr)
        self.assertNotIn("publish pages", pr)

        push = text.split("  cad_ci_push:", 1)[1]
        self.assertIn(
            "github.event_name == 'push' || github.event_name == 'workflow_dispatch'",
            push,
        )
        self.assertEqual(push.count("runs-on: ubuntu-latest"), 1)
        self.assertIn(
            "group: forge-push-${{ github.repository }}-${{ github.ref_name }}",
            push,
        )
        self.assertIn("cancel-in-progress: true", push)
        self.assertIn("contents: write", push)
        self.assertIn("packages: read", push)
        self.assertIn("id: cad_ci", push)
        self.assertIn("source_sha: ${{ github.sha }}", push)
        self.assertIn("durable_scope: ${{ github.ref_name }}", push)
        self.assertIn("source_ref: ${{ github.ref_name }}", push)
        self.assertIn(
            "BUILD_COMMIT: ${{ steps.cad_ci.outputs.build_commit }}",
            push,
        )
        self.assertIn(
            "SCOPE: ${{ steps.cad_ci.outputs.scope }}",
            push,
        )
        self.assertIn(
            "PREPARED_SCOPE: ${{ steps.cad_ci.outputs.prepared_scope }}",
            push,
        )
        self.assertIn('--build-evidence "$PREPARED_SCOPE"', push)
        self.assertIn('--build-scope "$SCOPE"', push)
        self.assertIn('--build-commit "$BUILD_COMMIT"', push)
        self.assertIn("--preserve-subtree dev-cad", push)
        self.assertIn("--preserve-subtree dev-ci", push)
        self.assertIn('page_args=(--name "$SCOPE")', push)
        self.assertIn("python -m cad_ci_tool publish pages", push)
        self.assertIn('--source-ref "$SOURCE_REF"', push)
        self.assertIn('--expected-source "$SOURCE_SHA"', push)

        for retired in (
            "Resolve durable source scope",
            "python -m cad_ci_tool build fetch",
            "python -m cad_ci_tool build update-main",
            "python -m cad_ci_tool build update-named",
            "python -m cad_ci_tool build prepare-named",
            "python -m cad_ci_tool publish build",
            "FETCH_HEAD:$SOURCE_SCOPE/build.json",
            "scope_exists=false",
            "base_sha=$SOURCE_SHA",
        ):
            with self.subTest(retired=retired):
                self.assertNotIn(retired, push)

        self.assertNotIn("reusable-ci.yml@", text)
        self.assertNotIn("reusable-pr.yml@", text)
        self.assertNotIn("actions/upload-artifact", text)
        self.assertNotIn("actions/download-artifact", text)
        self.assertNotIn("actions/setup-python", text)
        self.assertNotIn("pip install", text)
        self.assertNotIn("publish_main_build:", text)
        self.assertNotIn("publish_stable_pages:", text)
        self.assertNotIn("runtime_check:", text)
        self.assertNotIn("environment_json:", text)
        self.assertNotIn("solidcraft_runtime.py", text)


if __name__ == "__main__":
    unittest.main()
