"""Tests for the explicit Forge release-publication policy."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE_PATH = Path(__file__).with_name("validate_release.py")
SPEC = importlib.util.spec_from_file_location("forge_validate_release", MODULE_PATH)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validator)

TARGET = "a" * 40


def documents(*, build_source=TARGET, release_source=TARGET, page_source=TARGET):
    return {
        (TARGET, validator.BLOCKERS_PATH): "# no active blockers\n",
        (TARGET, "scpf/pyproject.toml"): (
            '[project]\nname = "scpf"\nversion = "0.11.0"\n'
        ),
        (TARGET, "CHANGELOG.md"): (
            "# Changelog\n\n"
            "## [Unreleased]\n\n"
            "## [0.11.0] - 2026-11-22\n\n"
            "### Added\n\n- release candidate\n\n"
            "## [0.10.0] - 2026-11-18\n"
        ),
        (TARGET, "scpf/scpf/version.py"): (
            'TESTED_SOLIDCRAFT_VERSION = "0.45.0"\n'
        ),
        ("origin/build", validator.BUILD_MANIFEST_PATH): json.dumps(
            {
                "schema": 1,
                "scope": "main",
                "source_commit": build_source,
                "items": {
                    "ci/forge-release": {
                        "source_commit": release_source,
                        "final_step": "tool_verify",
                    }
                },
            }
        ),
        ("origin/gh-pages", validator.PAGES_PROVENANCE_PATH): json.dumps(
            {
                "source_commit": page_source,
                "build_manifest_source_commit": page_source,
            }
        ),
    }


class ReleaseValidatorTests(unittest.TestCase):
    def run_validate(self, docs):
        with tempfile.TemporaryDirectory() as temp:
            notes = Path(temp) / "notes.md"
            with (
                patch.object(validator, "git", return_value=TARGET),
                patch.object(
                    validator,
                    "read_at",
                    side_effect=lambda ref, path: docs[(ref, path)],
                ),
            ):
                solidcraft = validator.validate("0.11.0", TARGET, notes)
                return solidcraft, notes.read_text(encoding="utf-8")

    def test_accepts_exact_main_durable_candidate(self):
        solidcraft, notes = self.run_validate(documents())
        self.assertEqual(solidcraft, "0.45.0")
        self.assertIn("## [0.11.0] - 2026-11-22", notes)
        self.assertNotIn("## [0.10.0]", notes)

    def test_rejects_main_sha_mismatch(self):
        with tempfile.TemporaryDirectory() as temp:
            notes = Path(temp) / "notes.md"
            with patch.object(validator, "git", return_value="b" * 40):
                with self.assertRaisesRegex(SystemExit, "current main HEAD"):
                    validator.validate("0.11.0", TARGET, notes)

    def test_rejects_package_version_mismatch(self):
        docs = documents()
        docs[(TARGET, "scpf/pyproject.toml")] = (
            '[project]\nname = "scpf"\nversion = "0.10.0"\n'
        )
        with self.assertRaisesRegex(SystemExit, "package version mismatch"):
            self.run_validate(docs)

    def test_rejects_active_release_blocker(self):
        docs = documents()
        docs[(TARGET, validator.BLOCKERS_PATH)] = "# comment\nowner issue still open\n"
        with self.assertRaisesRegex(SystemExit, "release blocked"):
            self.run_validate(docs)

    def test_rejects_stale_durable_main(self):
        with self.assertRaisesRegex(SystemExit, "build/main source_commit"):
            self.run_validate(documents(build_source="b" * 40))

    def test_rejects_stale_forge_release_evidence(self):
        with self.assertRaisesRegex(SystemExit, "forge-release evidence"):
            self.run_validate(documents(release_source="b" * 40))

    def test_rejects_stale_stable_pages(self):
        with self.assertRaisesRegex(SystemExit, "stable Pages source_commit"):
            self.run_validate(documents(page_source="b" * 40))

    def test_rejects_undated_release_section(self):
        docs = documents()
        docs[(TARGET, "CHANGELOG.md")] = (
            "# Changelog\n\n## [Unreleased]\n\n### Added\n- work\n"
        )
        with self.assertRaisesRegex(SystemExit, "no dated"):
            self.run_validate(docs)

    def test_forge_release_item_watches_release_candidate_metadata(self):
        root = Path(__file__).resolve().parents[2]
        contract = (root / "ci/forge-release/ci.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("ci/forge-release/ci.yml", contract)
        self.assertIn("CHANGELOG.md", contract)

    def test_workflow_is_explicit_owner_trigger_not_automatic(self):
        root = Path(__file__).resolve().parents[2]
        workflow = (root / ".github/workflows/release.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("issue_comment:", workflow)
        self.assertIn("github.actor == github.repository_owner", workflow)
        self.assertIn("/release ", workflow)
        self.assertIn("scripts/release/publish_release.py", workflow)
        self.assertNotIn("gh release create", workflow)
        self.assertNotIn("git tag -a", workflow)
        self.assertNotIn("workflow_run:", workflow)


if __name__ == "__main__":
    unittest.main()
