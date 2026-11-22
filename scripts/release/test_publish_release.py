"""Tests for Forge release tag/publication state handling."""

from __future__ import annotations

import importlib.util
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

MODULE_PATH = Path(__file__).with_name("publish_release.py")
SPEC = importlib.util.spec_from_file_location("forge_publish_release", MODULE_PATH)
publisher = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(publisher)

TARGET = "a" * 40


class PublishReleaseTests(unittest.TestCase):
    def test_absent_tag_is_not_treated_as_existing(self):
        with patch.object(publisher, "tag_target", return_value=None):
            self.assertFalse(publisher.verify_existing_tag("v0.11.0", TARGET))

    def test_conflicting_tag_is_rejected(self):
        with patch.object(publisher, "tag_target", return_value="b" * 40):
            with patch.object(publisher, "output", return_value="tag"):
                with self.assertRaisesRegex(SystemExit, "points to"):
                    publisher.verify_existing_tag("v0.11.0", TARGET)

    def test_lightweight_tag_is_rejected(self):
        with patch.object(publisher, "tag_target", return_value=TARGET):
            with patch.object(publisher, "output", return_value="commit"):
                with self.assertRaisesRegex(SystemExit, "not an annotated tag"):
                    publisher.verify_existing_tag("v0.11.0", TARGET)

    def test_existing_release_without_tag_is_rejected(self):
        with (
            patch.object(publisher, "fetch_release_inputs"),
            patch.object(publisher, "validate"),
            patch.object(publisher, "release_url", return_value="https://example.invalid/release"),
            patch.object(publisher, "verify_existing_tag", return_value=False),
            tempfile.TemporaryDirectory() as _,
        ):
            with self.assertRaisesRegex(SystemExit, "without the expected annotated tag"):
                publisher.publish(
                    repository="brainboxemb/lib.py.solidcraft.forge",
                    version="0.11.0",
                    target_sha=TARGET,
                )

    def test_matching_annotated_tag_is_accepted(self):
        with patch.object(publisher, "tag_target", return_value=TARGET):
            with patch.object(publisher, "output", return_value="tag"):
                self.assertTrue(
                    publisher.verify_existing_tag("v0.11.0", TARGET)
                )


if __name__ == "__main__":
    unittest.main()
