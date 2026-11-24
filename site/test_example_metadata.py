#!/usr/bin/env python3
"""Validate self-describing Forge example metadata."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scpf"))

from example_metadata import (
    discover_example_metadata,
    discover_verification_metadata,
    load_section_presentation,
)
from scpf.model_metadata import MODEL_METADATA_FIELDS
from example_documentation import (
    discover_example_documentation,
    discover_verification_documentation,
)


class ExampleMetadataTests(unittest.TestCase):
    def _assert_catalog_rows_are_self_describing(self, rows):
        for row in rows:
            with self.subTest(slug=row.slug, source_path=row.source_path):
                root = row.source_root
                self.assertTrue((root / "scpf" / "model.py").is_file())
                self.assertTrue((root / "verification" / "verify.py").is_file())
                self.assertGreaterEqual(len(row.stages), 1)
                self.assertTrue((root / "README.md").is_file())

    def _assert_documentation_is_complete_and_provenanced(
        self,
        metadata,
        documentation,
    ):
        metadata_by_slug = {row.slug: row for row in metadata}
        self.assertEqual(
            {row.slug for row in documentation},
            set(metadata_by_slug),
        )

        for row in documentation:
            with self.subTest(slug=row.slug):
                source = (
                    metadata_by_slug[row.slug].source_root / "README.md"
                ).read_text(encoding="utf-8")
                self.assertTrue(
                    "be40b09e7454a90e87d83768a9e7453c52ba5d76" in source
                    or "> Documentation provenance:" in source
                )
                self.assertTrue(row.title)
                self.assertTrue(row.group)
                self.assertTrue(row.goal)
                self.assertTrue(row.forge_api)
                self.assertTrue(row.forge_model)
                self.assertTrue(row.lowering)
                self.assertTrue(row.solidcraft_result)
                self.assertTrue(row.saved_design_test)
                self.assertIsInstance(row.bounds_sufficient, bool)
                self.assertTrue(row.geometry_reason)
                self.assertGreaterEqual(len(row.reference_notes), 1)

    def _public_metadata_rows(self):
        by_path = {}
        for row in (
            *discover_example_metadata(),
            *discover_verification_metadata(),
        ):
            by_path[row.source_path] = row
        return tuple(by_path[path] for path in sorted(by_path))

    def test_examples_and_verification_are_self_describing(self):
        examples = discover_example_metadata()
        verification = discover_verification_metadata()

        self.assertEqual(
            tuple(row.slug for row in examples),
            ("anchored-holes", "components", "corner-anchor", "simple-box"),
        )
        self.assertGreater(len(verification), len(examples))

        self._assert_catalog_rows_are_self_describing(examples)
        self._assert_catalog_rows_are_self_describing(verification)

    def test_preserved_public_documentation_is_complete_and_provenanced(self):
        self._assert_documentation_is_complete_and_provenanced(
            discover_example_metadata(),
            discover_example_documentation(),
        )
        self._assert_documentation_is_complete_and_provenanced(
            discover_verification_metadata(),
            discover_verification_documentation(),
        )

    def test_bracket_readme_describes_current_minimal_l_profile(self):
        metadata = {
            row.slug: row
            for row in discover_verification_metadata()
        }["bracket"]
        source = (metadata.source_root / "README.md").read_text(
            encoding="utf-8"
        )
        documentation = {
            row.slug: row
            for row in discover_verification_documentation()
        }["bracket"]

        self.assertIn("# Minimal L-profile", source)
        self.assertIn("**Group:** `fundamentals`", source)
        self.assertEqual(documentation.title, "Minimal L-profile")
        self.assertEqual(documentation.group, "fundamentals")
        self.assertNotIn("two mounting holes", source)
        self.assertNotIn("valid fillet point", source)
        self.assertNotIn("source/bracket.json", source)

    def test_model_yml_keeps_only_agreed_generic_fields(self):
        import yaml

        expected = set(MODEL_METADATA_FIELDS)
        for row in self._public_metadata_rows():
            with self.subTest(slug=row.slug, source_path=row.source_path):
                source = (row.source_root / "model.yml").read_text(
                    encoding="utf-8"
                )
                data = yaml.safe_load(source)
                self.assertEqual(set(data), expected)

    def test_verification_section_and_case_priorities_are_complete_and_deterministic(self):
        rows = discover_verification_metadata()
        sections = load_section_presentation()

        self.assertEqual(
            set(sections),
            {row.section for row in rows},
        )
        self.assertEqual(
            len(
                {
                    priority
                    for priority, _label, _description
                    in sections.values()
                }
            ),
            len(sections),
        )

        by_section = {}
        for row in rows:
            self.assertGreater(row.priority, 0)
            by_section.setdefault(row.section, []).append(row)

        for section, section_rows in by_section.items():
            with self.subTest(section=section):
                priorities = [row.priority for row in section_rows]
                self.assertEqual(len(priorities), len(set(priorities)))

    def test_teaching_examples_own_explicit_catalog_roles(self):
        import yaml

        roots = tuple(
            root
            for root in sorted((ROOT / "examples").iterdir())
            if root.is_dir()
        )
        self.assertEqual(len(roots), 4)

        for root in roots:
            with self.subTest(slug=root.name):
                self.assertTrue((root / "catalog.yml").is_file())
                self.assertFalse((root / "role.yml").exists())
                data = yaml.safe_load(
                    (root / "catalog.yml").read_text(encoding="utf-8")
                )
                self.assertEqual(data.get("schema"), 1)
                self.assertIs(data.get("public_example"), True)
                self.assertIsInstance(data.get("public_verification"), bool)
                for path in (
                    root / "ci.yml",
                    root / "model.yml",
                    root / "README.md",
                    root / "scpf" / "model.py",
                    root / "verification" / "verify.py",
                ):
                    self.assertTrue(path.is_file(), path.as_posix())

    def test_public_verification_cases_do_not_use_regression_roles(self):
        for root in sorted((ROOT / "verification" / "cases").iterdir()):
            if not root.is_dir():
                continue
            with self.subTest(slug=root.name):
                self.assertFalse((root / "role.yml").exists())
                for path in (
                    root / "ci.yml",
                    root / "model.yml",
                    root / "README.md",
                    root / "scpf" / "model.py",
                    root / "verification" / "verify.py",
                ):
                    self.assertTrue(path.is_file(), path.as_posix())

    def test_regression_directories_keep_explicit_non_public_roles(self):
        import yaml

        allowed_role_fields = {
            "schema",
            "role",
            "decision",
            "owner",
            "reason",
            "blocked_by",
        }
        allowed_roles = {
            "release-verification",
            "regression-fixture",
        }

        roots = tuple(
            root
            for root in sorted(
                (ROOT / "verification" / "regressions").iterdir()
            )
            if root.is_dir()
        )
        self.assertGreater(len(roots), 0)

        for root in roots:
            with self.subTest(slug=root.name):
                role_path = root / "role.yml"
                self.assertTrue(role_path.is_file())
                data = yaml.safe_load(role_path.read_text(encoding="utf-8"))
                self.assertIsInstance(data, dict)
                self.assertEqual(data.get("schema"), 1)
                self.assertIn(data.get("role"), allowed_roles)
                self.assertIsInstance(data.get("decision"), str)
                self.assertTrue(data["decision"].strip())
                self.assertIsInstance(data.get("owner"), str)
                self.assertTrue(data["owner"].strip())
                self.assertIsInstance(data.get("reason"), str)
                self.assertTrue(data["reason"].strip())
                self.assertFalse(set(data) - allowed_role_fields)

                if data["role"] == "release-verification":
                    self.assertEqual(data["decision"], "keep-blocked")
                    self.assertIsInstance(data.get("blocked_by"), str)
                else:
                    self.assertEqual(data["decision"], "keep")

    def test_metadata_never_claims_current_verification_status(self):
        forbidden = {"pass", "fail", "passed", "failed", "status"}
        for row in self._public_metadata_rows():
            with self.subTest(slug=row.slug, source_path=row.source_path):
                source = (row.source_root / "model.yml").read_text(
                    encoding="utf-8"
                ).lower()
                for token in forbidden:
                    self.assertNotIn(f"{token}:", source)


if __name__ == "__main__":
    unittest.main()
