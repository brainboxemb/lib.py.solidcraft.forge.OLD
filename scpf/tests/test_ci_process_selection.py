"""Guard current Verification model processing."""

from pathlib import Path
import re
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / "examples"


class CiProcessSelectionContractTests(unittest.TestCase):
    """Keep every current full Verification model visible to CAD-CI."""

    def test_all_verification_models_are_processed(self):
        """Match processed model items to distributed model.yml membership."""

        configured = {}
        for ci_path in sorted(EXAMPLES.glob("*/ci.yml")):
            text = ci_path.read_text(encoding="utf-8")
            match = re.search(
                r"^process:\s*(true|false)\s*$",
                text,
                re.MULTILINE,
            )
            self.assertIsNotNone(
                match,
                f"missing explicit process declaration: {ci_path}",
            )
            configured[ci_path.parent.name] = match.group(1) == "true"

        expected = {
            path.parent.name
            for path in EXAMPLES.glob("*/model.yml")
        }
        self.assertTrue(expected.issubset(configured))
        self.assertTrue(
            all(configured[slug] for slug in expected),
            "every public Verification model must be process:true",
        )

        extras = set(configured) - expected
        for slug in sorted(extras):
            role_path = EXAMPLES / slug / "role.yml"
            self.assertTrue(role_path.is_file(), role_path)
            role = yaml.safe_load(role_path.read_text(encoding="utf-8"))
            self.assertEqual(role.get("role"), "regression-fixture")
            self.assertEqual(role.get("decision"), "keep")


if __name__ == "__main__":
    unittest.main()
