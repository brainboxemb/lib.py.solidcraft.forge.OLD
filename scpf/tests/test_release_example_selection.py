"""Tests for purpose-driven Forge basic model selection."""

from pathlib import Path
import tempfile
import unittest

from scripts.model_selection import example_slugs


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "scpf"


def model_yaml(purpose: str) -> str:
    return f"""purpose: {purpose}
section: fundamentals
priority: 10
title: Test model
tagline: Test tagline
description: Test description
parameters: none
stages:
  - Build
"""


class ReleaseExampleSelectionTests(unittest.TestCase):
    def test_example_purpose_selects_scalar_and_list_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            examples = root / "examples"
            for slug, purpose in (
                ("z-verification", "verification"),
                ("b-both", "[verification, example]"),
                ("a-example", "example"),
            ):
                model = examples / slug / "model.yml"
                model.parent.mkdir(parents=True)
                model.write_text(model_yaml(purpose), encoding="utf-8")

            self.assertEqual(
                example_slugs(PACKAGE, root),
                ("a-example", "b-both"),
            )

    def test_verification_only_models_do_not_enter_basic_set(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            model = root / "examples" / "only" / "model.yml"
            model.parent.mkdir(parents=True)
            model.write_text(model_yaml("verification"), encoding="utf-8")

            with self.assertRaisesRegex(RuntimeError, "selects no Example"):
                example_slugs(PACKAGE, root)


if __name__ == "__main__":
    unittest.main()
