#!/usr/bin/env python3
"""Render Forge Pages from CAD-CI supplied durable publication context."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[3]


def required(name: str) -> str:
    """Return one required CAD-CI publication value."""

    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"{name} is required")
    return value


def main() -> int:
    """Build and validate one complete Forge Pages tree."""

    output_root = Path(required("CAD_CI_OUTPUT")).resolve()
    complete_scope = Path(required("CAD_CI_COMPLETE_SCOPE")).resolve()
    build_scope = required("CAD_CI_BUILD_SCOPE")
    source_sha = required("CAD_CI_SOURCE_SHA")
    build_commit = required("CAD_CI_BUILD_COMMIT")

    site = output_root / "site"
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "site" / "build.py"),
            "--out",
            str(site),
            "--source-sha",
            source_sha,
            "--build-evidence",
            str(complete_scope),
            "--build-scope",
            build_scope,
            "--build-commit",
            build_commit,
        ],
        cwd=ROOT,
        check=True,
    )

    provenance_path = site / "provenance.json"
    manifest_path = site / "verification" / "manifest.json"
    if not provenance_path.is_file() or provenance_path.stat().st_size <= 0:
        raise RuntimeError("Pages builder did not produce provenance.json")
    if not manifest_path.is_file() or manifest_path.stat().st_size <= 0:
        raise RuntimeError(
            "Pages builder did not produce verification/manifest.json"
        )

    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    expected = {
        "source_commit": source_sha,
        "build_commit": build_commit,
        "build_scope": build_scope,
    }
    for key, value in expected.items():
        if provenance.get(key) != value:
            raise RuntimeError(
                f"Pages provenance mismatch for {key}: "
                f"{provenance.get(key)!r} != {value!r}"
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
