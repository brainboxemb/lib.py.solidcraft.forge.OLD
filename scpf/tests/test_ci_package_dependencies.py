"""Guard Forge package, builder and verification dependency ownership."""

from pathlib import Path
import re
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "scpf" / "ci.yml"
TESTS = ROOT / "ci" / "forge-tests" / "ci.yml"
RELEASE = ROOT / "ci" / "forge-release" / "ci.yml"
EXAMPLES = ROOT / "examples"
BUILDERS = ROOT / "ci" / "builders"


def needs(text: str) -> set[str]:
    """Return the simple top-level needs list from one Forge ci.yml."""

    match = re.search(
        r"^needs:\s*\n((?:  - [^\n]+\n)+)",
        text,
        re.MULTILINE,
    )
    if match is None:
        return set()
    return {
        line.removeprefix("  - ").strip()
        for line in match.group(1).splitlines()
    }


class CiPackageDependencyContractTests(unittest.TestCase):
    """Keep item config declarative and executable behavior builder-owned."""

    def test_package_item_selects_only_package_builder(self):
        item = PACKAGE.read_text(encoding="utf-8")
        builder = (
            BUILDERS / "forge-package" / "builder.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("id: forge-package", item)
        self.assertIn("builder: forge-package", item)
        self.assertNotIn("steps:", item)
        self.assertIn("- id: tool_build", builder)
        self.assertIn("outputs: [dist]", builder)
        self.assertNotIn("- id: tool_test", builder)
        self.assertNotIn("- id: tool_verify", builder)

    def test_unit_tests_depend_only_on_package(self):
        item = TESTS.read_text(encoding="utf-8")
        builder = (
            BUILDERS / "forge-tests" / "builder.yml"
        ).read_text(encoding="utf-8")
        self.assertEqual(needs(item), {"forge-package"})
        self.assertIn("builder: forge-tests", item)
        self.assertNotIn("steps:", item)
        self.assertIn("- id: tool_test", builder)
        self.assertNotIn("tool_build", builder)
        self.assertNotIn("tool_verify", builder)

    def test_release_verification_depends_only_on_package(self):
        item = RELEASE.read_text(encoding="utf-8")
        builder = (
            BUILDERS / "forge-release" / "builder.yml"
        ).read_text(encoding="utf-8")
        self.assertEqual(needs(item), {"forge-package"})
        self.assertIn("builder: forge-release", item)
        self.assertNotIn("steps:", item)
        self.assertIn("- id: tool_verify", builder)
        self.assertNotIn("tool_build", builder)
        self.assertNotIn("tool_test", builder)

    def test_every_model_uses_one_shared_declarative_template(self):
        expected = {
            path.parent.name
            for path in EXAMPLES.glob("*/model.yml")
        }
        configs = {
            path.parent.name: path
            for path in EXAMPLES.glob("*/ci.yml")
        }
        self.assertTrue(expected.issubset(configs))
        extras = set(configs) - expected
        for slug in sorted(extras):
            role_path = EXAMPLES / slug / "role.yml"
            self.assertTrue(role_path.is_file(), role_path)
            role = yaml.safe_load(role_path.read_text(encoding="utf-8"))
            self.assertEqual(role.get("role"), "regression-fixture")
            self.assertEqual(role.get("decision"), "keep")

        root_ci = (ROOT / "cad-ci.yml").read_text(encoding="utf-8")
        self.assertIn("  forge-model-declarative:", root_ci)
        self.assertIn("    builder: forge-model", root_ci)
        self.assertIn("      - forge-package", root_ci)
        self.assertIn("      - model-verification-batch", root_ci)

        for slug, path in sorted(configs.items()):
            with self.subTest(slug=slug, path=path):
                text = path.read_text(encoding="utf-8")
                self.assertIn("template: forge-model-declarative", text)
                self.assertNotIn("steps:", text)
                self.assertNotIn("run:", text)
                self.assertNotIn("copy:", text)

    def test_verification_batches_request_public_owner_package(self):
        model_batch = (
            ROOT / "ci" / "model-verification-batch" / "ci.yml"
        ).read_text(encoding="utf-8")
        reference_batch = (
            ROOT / "ci" / "reference-verification-batch" / "ci.yml"
        ).read_text(encoding="utf-8")
        model_builder = (
            BUILDERS / "model-verification-batch" / "builder.yml"
        ).read_text(encoding="utf-8")
        reference_builder = (
            BUILDERS / "reference-verification-batch" / "builder.yml"
        ).read_text(encoding="utf-8")

        self.assertEqual(needs(model_batch), {"forge-package"})
        self.assertEqual(needs(reference_batch), set())
        self.assertNotIn("cad-ci-verification-package", model_batch)
        self.assertNotIn("cad-ci-verification-package", reference_batch)
        self.assertIn("verification_package: true", model_builder)
        self.assertIn("verification_package: true", reference_builder)
        self.assertFalse((ROOT / "ci" / "cad-verification-package").exists())

    def test_root_manifest_owns_builders_and_generic_verification(self):
        text = (ROOT / "cad-ci.yml").read_text(encoding="utf-8")
        self.assertIn("  - scpf\n", text)
        self.assertIn("  - ci/*\n", text)
        self.assertIn("builders:", text)
        self.assertIn("forge-model: ci/builders/forge-model", text)
        self.assertIn("verification:", text)
        self.assertIn("runtimes:", text)
        self.assertIn('reference: "ghcr.io/brainboxemb/cad-reference:v0.3.5"', text)

    def test_consumers_resolve_dependency_wheels_without_packaging_them(self):
        tool_ci = (ROOT / "scripts" / "tool_ci.py").read_text(encoding="utf-8")
        tool_verify = (
            ROOT / "scripts" / "tool_verify.py"
        ).read_text(encoding="utf-8")
        forge_example = (
            ROOT / "scripts" / "forge_example.py"
        ).read_text(encoding="utf-8")

        self.assertIn('dependency_wheel("forge-package")', tool_ci)
        self.assertIn('dependency_wheel("forge-package")', tool_verify)
        self.assertIn("def dependency_wheel(", forge_example)
        self.assertIn("def verification_wheel(", forge_example)
        self.assertIn("CAD_CI_VERIFICATION_WHEEL", forge_example)
        self.assertFalse((ROOT / "scripts" / "verification_package.py").exists())


if __name__ == "__main__":
    unittest.main()
