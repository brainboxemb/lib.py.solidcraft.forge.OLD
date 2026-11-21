from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
CAPTURE = ROOT / "scripts" / "capture_solidcraft_reference.py"

spec = importlib.util.spec_from_file_location(
    "capture_solidcraft_reference",
    CAPTURE,
)
assert spec is not None and spec.loader is not None
capture = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = capture
spec.loader.exec_module(capture)


def registry():
    required = [
        "engine.commands",
        "solid.box",
        "solid.extrude",
        "sketch.create",
        "sketch.draw.dimensioned",
        "sketch.slot.center_to_center",
    ]
    rows = [
        {
            "id": command_id,
            "label": command_id,
            "tab": "",
            "panel": "",
            "icon": "",
            "shortcut": None,
            "params": "",
            "enabled": True,
            "disabled_reason": None,
        }
        for command_id in required
    ]
    for index in range(capture.MIN_COMMAND_COUNT - len(rows)):
        rows.append(
            {
                "id": f"test.command_{index:03d}",
                "label": f"Test command {index:03d}",
                "tab": "TEST",
                "panel": "COMMANDS",
                "icon": "",
                "shortcut": None,
                "params": "",
                "enabled": True,
                "disabled_reason": None,
            }
        )
    return rows


class SolidCraftReferenceCaptureTests(unittest.TestCase):
    def test_rejects_small_hand_curated_registry(self):
        with self.assertRaisesRegex(ValueError, "implausibly small"):
            capture.validate_registry(
                [
                    {"id": "solid.box", "label": "Box"},
                    {"id": "sketch.slot.center_to_center", "label": "Slot"},
                ]
            )

    def test_rejects_missing_required_commands(self):
        rows = registry()
        rows = [row for row in rows if row["id"] != "engine.commands"]
        rows.append(
            {
                "id": "test.replacement",
                "label": "Replacement",
            }
        )
        with self.assertRaisesRegex(ValueError, "required SolidCraft commands"):
            capture.validate_registry(rows)

    def test_snapshot_keeps_raw_registry_and_generated_catalog_in_lockstep(self):
        rows = capture.validate_registry(registry())
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "0.45.0"
            capture.write_snapshot(
                out=out,
                version="0.45.0",
                cli_version="solidcraft-cli 0.45.0",
                upstream_commit="e8ce12ef78fe76281a04b7242a9ce059ff7d5067",
                runtime_release="v0.3.4",
                runtime_image="ghcr.io/brainboxemb/cad-solidcraft:v0.3.4",
                commands=rows,
            )

            raw = json.loads(
                (out / "commands.json").read_text(encoding="utf-8")
            )
            markdown = (out / "commands.md").read_text(encoding="utf-8")
            source = (out / "SOURCE.md").read_text(encoding="utf-8")

            self.assertEqual(len(raw), capture.MIN_COMMAND_COUNT)
            self.assertIn(
                f"Total registered commands: **{capture.MIN_COMMAND_COUNT}**.",
                markdown,
            )
            for row in raw:
                self.assertIn(f"`{row['id']}`", markdown)
            self.assertIn("v0.3.4", source)
            self.assertIn("solidcraft-cli 0.45.0", source)

    def test_discarded_043_reference_tree_is_absent(self):
        self.assertFalse(
            (ROOT / "docs" / "reference" / "solidcraft" / "0.43.0").exists()
        )


if __name__ == "__main__":
    unittest.main()
