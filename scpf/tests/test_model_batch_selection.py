"""Contracts for Forge consumption of CAD-CI active model dependents."""

from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import model_verification_batch as batch  # noqa: E402


class ModelBatchSelectionTests(unittest.TestCase):
    def test_ci_item_opts_into_direct_dependent_context(self):
        text = (
            ROOT / "ci" / "model-verification-batch" / "ci.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("selection_context: direct_dependents", text)

        reference = (
            ROOT / "ci" / "reference-verification-batch" / "ci.yml"
        ).read_text(encoding="utf-8")
        self.assertNotIn("selection_context:", reference)

    def test_active_model_ids_preserve_cad_ci_order(self):
        with patch.dict(
            os.environ,
            {
                "CAD_CI_ACTIVE_DEPENDENTS_JSON": json.dumps(
                    ["plate", "simple-box"]
                )
            },
            clear=False,
        ):
            self.assertEqual(
                batch.active_declarative_slugs(
                    ("simple-box", "plate", "slot-family")
                ),
                ("plate", "simple-box"),
            )

    def test_unknown_or_invalid_context_is_rejected(self):
        cases = (
            '["simple-box", "not-a-model"]',
            '["simple-box", "simple-box"]',
            '{"item": "simple-box"}',
            '[""]',
            'not-json',
        )
        for raw in cases:
            with self.subTest(raw=raw), patch.dict(
                os.environ,
                {"CAD_CI_ACTIVE_DEPENDENTS_JSON": raw},
                clear=False,
            ), self.assertRaises(RuntimeError):
                batch.active_declarative_slugs(("simple-box", "plate"))

        with patch.dict(os.environ, {}, clear=True), self.assertRaisesRegex(
            RuntimeError,
            "CAD_CI_ACTIVE_DEPENDENTS_JSON is required",
        ):
            batch.active_declarative_slugs(("simple-box",))

    def test_empty_direct_dependents_skip_runtime_and_dependencies(self):
        with tempfile.TemporaryDirectory() as tmp:
            with (
                patch.object(batch, "output_root", return_value=Path(tmp)),
                patch.object(batch, "active_declarative_slugs", return_value=()),
                patch.object(batch, "dependency_wheel") as dependency_wheel,
                patch.object(batch.subprocess, "run") as subprocess_run,
            ):
                self.assertEqual(batch.run_host_batch(), 0)

            dependency_wheel.assert_not_called()
            subprocess_run.assert_not_called()
            self.assertTrue((Path(tmp) / "items").is_dir())


if __name__ == "__main__":
    unittest.main()
