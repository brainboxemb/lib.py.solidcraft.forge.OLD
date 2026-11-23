from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]


def load_script(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


forge_example = load_script("forge_example_ci_test", "scripts/forge_example.py")


class CiDependencyTests(unittest.TestCase):
    def test_dependency_wheel_supports_owner_package_dependency(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            forge = root / "forge"
            verification = root / "verification"
            (forge / "dist").mkdir(parents=True)
            (verification / "dist").mkdir(parents=True)
            forge_wheel = forge / "dist" / "scpf-0.11.0-py3-none-any.whl"
            verification_wheel = (
                verification
                / "dist"
                / "brainboxemb_cad_verification_lib-0.16.0-py3-none-any.whl"
            )
            forge_wheel.write_bytes(b"forge")
            verification_wheel.write_bytes(b"verification")
            dependencies = {
                "forge-package": {"output_root": str(forge)},
                "cad-ci-verification-package": {
                    "output_root": str(verification)
                },
            }
            with patch.dict(
                os.environ,
                {"CAD_CI_DEPENDENCIES_JSON": json.dumps(dependencies)},
                clear=False,
            ):
                self.assertEqual(
                    forge_example.dependency_wheel(),
                    forge_wheel.resolve(),
                )
                self.assertEqual(
                    forge_example.dependency_wheel(
                        "cad-ci-verification-package",
                        "brainboxemb_cad_verification_lib-*.whl",
                    ),
                    verification_wheel.resolve(),
                )

    def test_verification_package_is_root_pinned_and_not_forge_built(self):
        config = (ROOT / "cad-ci.yml").read_text(encoding="utf-8")
        self.assertIn("verification:", config)
        self.assertIn(
            "repository: brainboxemb/lib.py.cad.verification",
            config,
        )
        self.assertIn('version: "0.16.0"', config)
        self.assertIn(
            "commit: c7c145b7be0c602724e8cca874ef29990baaad1e",
            config,
        )
        self.assertFalse((ROOT / "scripts" / "verification_package.py").exists())
        self.assertFalse((ROOT / "ci" / "cad-verification-package").exists())


if __name__ == "__main__":
    unittest.main()
