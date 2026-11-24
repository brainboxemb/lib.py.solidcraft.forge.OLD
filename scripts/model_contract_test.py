#!/usr/bin/env python3
"""Run one model item's command-contract tests against the exact Forge package."""

from __future__ import annotations

import os

from forge_example import dependency_wheel, run_contract_tests


def item_path() -> str:
    """Return the repository path selected by CAD-CI."""

    value = os.environ.get("CAD_CI_ITEM_PATH", "").strip()
    if not value:
        raise RuntimeError("CAD_CI_ITEM_PATH is required")
    return value


def main() -> int:
    """Run the selected model's contract tests with the dependency wheel."""

    run_contract_tests(item_path(), dependency_wheel())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
