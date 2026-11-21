#!/usr/bin/env python3
"""Verify one checked SolidCraft command snapshot against an immutable runtime."""

from __future__ import annotations

import argparse
import base64
import gzip
import json
from pathlib import Path
import subprocess
import sys

from capture_solidcraft_reference import validate_registry


ROOT = Path(__file__).resolve().parents[1]


def runtime_output(image: str, *command: str) -> str:
    completed = subprocess.run(
        ["docker", "run", "--rm", "--pull=never", image, *command],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return completed.stdout


def normalized_registry(text: str) -> list[dict]:
    rows = validate_registry(json.loads(text))
    return sorted(rows, key=lambda row: str(row["id"]))


def bootstrap_line(rows: list[dict]) -> str:
    raw = (json.dumps(rows, indent=2, sort_keys=True) + "\n").encode("utf-8")
    payload = base64.b64encode(gzip.compress(raw, mtime=0)).decode("ascii")
    return f"SOLIDCRAFT_REFERENCE_GZIP_BASE64={payload}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--snapshot", type=Path, required=True)
    args = parser.parse_args()

    subprocess.run(["docker", "pull", args.image], check=True)

    version_text = runtime_output(args.image, "solidcraft-cli", "--version").strip()
    if args.version not in version_text:
        raise SystemExit(
            f"runtime version mismatch: expected {args.version!r} in {version_text!r}"
        )

    rows = normalized_registry(
        runtime_output(args.image, "solidcraft-cli", "commands")
    )

    snapshot = ROOT / args.snapshot
    if not snapshot.is_file():
        print(bootstrap_line(rows))
        raise SystemExit(
            f"missing canonical snapshot: {args.snapshot}; "
            "capture the emitted runtime registry and rerun"
        )

    expected = normalized_registry(snapshot.read_text(encoding="utf-8"))
    if expected != rows:
        print(bootstrap_line(rows))
        raise SystemExit(
            f"canonical snapshot differs from {args.image}; "
            "runtime registry emitted for audit"
        )

    print(
        f"SolidCraft reference matches {args.image}: "
        f"{version_text}; {len(rows)} commands"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
