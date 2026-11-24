#!/usr/bin/env python3
"""Validate self-describing Forge model catalog metadata."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scpf"))

from example_metadata import (
    discover_example_metadata,
    discover_model_metadata,
    discover_verification_metadata,
    load_section_presentation,
)
from scpf.model_metadata import MODEL_METADATA_FIELDS, MODEL_PURPOSES
from example_documentation import (
    discover_example_documentation,
    discover_verification_documentation,
)


class ExampleMetadataTests(unittest.TestCase):
    def _assert_rows_are_self_describing(self, rows):
        for row in rows:
            with self.subTest(slug=row.slug):
                root = ROOT / "examples" / row.slug
                self.assertTrue((root / "scpf" / "model.py").is_file())
                self.assertTrue((root / "verification" / "verify.py").is_file())
                self.assertGreaterEqual(len(row.stages), 1)
                self.assertTrue((root / "README.md").is_file())

    def _assert_documentation(self, metadata, documentation):
        self.assertEqual(
            {row.slug for row in documentation},
            {row.slug for row in metadata},
        )
        for row in documentation:
            with self.subTest(slug=row.slug):
                source = (
                    ROOT / "examples" / row.slug / "README.md"
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

    def test_purpose_selects_exact_curated_examples(self):
        rows = discover_example_metadata()
        self.assertEqual(
            tuple(row.slug for row in rows),
            ("anchored-holes", "components", "corner-anchor", "simple-box"),
        )
        for row in rows:
            self.assertEqual(row.purpose, {"example", "verification"})
        self._assert_rows_are_self_describing(rows)

    def test_verification_catalog_is_broader_and_self_describing(self):
        rows = discover_verification_metadata()
        slugs = {row.slug for row in rows}
        self.assertGreater(len(rows), len(discover_example_metadata()))
        for slug in (
            "attached-through-all",
            "rotated-sketch-cutter",
            "sheet-contour-flange",
            "sheet-edge-flange",
            "sheet-fold",
            "sheet-hem",
            "sheet-path-flange",
        ):
            self.assertIn(slug, slugs)
        self._assert_rows_are_self_describing(rows)

    def test_preserved_public_documentation_matches_each_purpose(self):
        self._assert_documentation(
            discover_example_metadata(),
            discover_example_documentation(),
        )
        self._assert_documentation(
            discover_verification_metadata(),
            discover_verification_documentation(),
        )

    def test_bracket_readme_describes_current_minimal_l_profile(self):
        root = ROOT / "examples" / "bracket"
        source = (root / "README.md").read_text(encoding="utf-8")
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

    def test_model_yml_keeps_only_canonical_shared_fields(self):
        import yaml

        expected = set(MODEL_METADATA_FIELDS)
        for row in discover_model_metadata():
            with self.subTest(slug=row.slug):
                source = (
                    ROOT / "examples" / row.slug / "model.yml"
                ).read_text(encoding="utf-8")
                data = yaml.safe_load(source)
                self.assertEqual(set(data), expected)
                self.assertTrue(row.purpose)
                self.assertTrue(row.purpose.issubset(MODEL_PURPOSES))

    def test_verification_section_and_case_priorities_are_deterministic(self):
        rows = discover_verification_metadata()
        sections = load_section_presentation()

        self.assertEqual(set(sections), {row.section for row in rows})
        self.assertIn("sheet-metal", sections)
        self.assertEqual(
            len({priority for priority, _label, _description in sections.values()}),
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

    def test_catalog_membership_is_not_a_second_catalog_file(self):
        self.assertFalse(tuple((ROOT / "examples").glob("*/catalog.yml")))
        for row in discover_model_metadata():
            with self.subTest(slug=row.slug):
                self.assertTrue(row.purpose)

    def test_promoted_public_cases_do_not_keep_regression_role_files(self):
        for slug in (
            "attached-through-all",
            "rotated-sketch-cutter",
            "sheet-contour-flange",
            "sheet-edge-flange",
            "sheet-hem",
            "sheet-path-flange",
        ):
            self.assertFalse((ROOT / "examples" / slug / "role.yml").exists())

    def test_metadata_never_claims_current_verification_status(self):
        forbidden = {"pass", "fail", "passed", "failed", "status"}
        for row in discover_model_metadata():
            with self.subTest(slug=row.slug):
                source = (
                    ROOT / "examples" / row.slug / "model.yml"
                ).read_text(encoding="utf-8").lower()
                for token in forbidden:
                    self.assertNotIn(f"{token}:", source)


if __name__ == "__main__":
    unittest.main()
