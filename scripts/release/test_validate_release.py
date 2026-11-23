"""Tests for Forge-owned release validation."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("validate_release.py")
SPEC = importlib.util.spec_from_file_location(
    "forge_validate_release", MODULE_PATH
)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validator)

TARGET = "a" * 40


def write_candidate(root: Path, *, package_version="0.12.0", blockers=""):
    (root / "docs/background/design").mkdir(parents=True)
    (root / "docs/background/design/release-blockers.txt").write_text(
        blockers or "# no active blockers\n",
        encoding="utf-8",
    )
    (root / "scpf/scpf").mkdir(parents=True)
    (root / "scpf/pyproject.toml").write_text(
        '[project]\nname = "scpf"\n'
        f'version = "{package_version}"\n',
        encoding="utf-8",
    )
    (root / "scpf/scpf/version.py").write_text(
        'TESTED_SOLIDCRAFT_VERSION = "0.45.0"\n',
        encoding="utf-8",
    )
    (root / "CHANGELOG.md").write_text(
        "# Changelog\n\n"
        "## [Unreleased]\n\n"
        "## [0.12.0] - 2026-11-23\n\n"
        "### Added\n\n- release candidate\n\n"
        "## [0.11.0] - 2026-11-22\n",
        encoding="utf-8",
    )


class ReleaseValidatorTests(unittest.TestCase):
    def run_validate(self, **candidate):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_candidate(root, **candidate)
            notes = root / "notes.md"
            solidcraft = validator.validate(
                "0.12.0",
                TARGET,
                notes,
                root=root,
            )
            return solidcraft, notes.read_text(encoding="utf-8")

    def test_accepts_forge_specific_release_metadata(self):
        solidcraft, notes = self.run_validate()
        self.assertEqual(solidcraft, "0.45.0")
        self.assertIn("## [0.12.0] - 2026-11-23", notes)
        self.assertNotIn("## [0.11.0]", notes)

    def test_rejects_package_version_mismatch(self):
        with self.assertRaisesRegex(SystemExit, "package version mismatch"):
            self.run_validate(package_version="0.11.0")

    def test_rejects_active_release_blocker(self):
        with self.assertRaisesRegex(SystemExit, "release blocked"):
            self.run_validate(blockers="owner issue still open\n")

    def test_rejects_undated_release_section(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_candidate(root)
            (root / "CHANGELOG.md").write_text(
                "# Changelog\n\n## [Unreleased]\n\n"
                "### Added\n- work\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(SystemExit, "no dated"):
                validator.validate(
                    "0.12.0",
                    TARGET,
                    root / "notes.md",
                    root=root,
                )

    def test_validator_has_no_generic_build_or_pages_checks(self):
        source = MODULE_PATH.read_text(encoding="utf-8")
        self.assertNotIn("origin/build", source)
        self.assertNotIn("origin/gh-pages", source)
        self.assertNotIn("build.json", source)
        self.assertNotIn("provenance.json", source)
        self.assertNotIn("subprocess", source)

    def test_release_wrapper_uses_exact_shared_cad_release(self):
        root = Path(__file__).resolve().parents[2]
        workflow = (root / ".github/workflows/release.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "tool.cad.ci/.github/workflows/reusable-release.yml@v0.36.1",
            workflow,
        )
        self.assertIn(
            "validator_path: scripts/release/validate_release.py",
            workflow,
        )
        self.assertIn("build_branch: build", workflow)
        self.assertNotIn("publish_release.py", workflow)
        self.assertNotIn("gh-pages", workflow)
        self.assertNotIn("git tag", workflow)
        self.assertNotIn("gh release", workflow)


if __name__ == "__main__":
    unittest.main()
