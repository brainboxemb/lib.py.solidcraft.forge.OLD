#!/usr/bin/env python3
"""Run one model item's command-contract tests against the exact Forge package."""

from __future__ import annotations

import os
from pathlib import Path

from forge_example import dependency_wheel, run_contract_tests


def item_path() -> str:
    """Return CAD-CI's selected item as a repository-relative source path."""

    value = os.environ.get("CAD_CI_ITEM_PATH", "").strip()
    repo_value = os.environ.get("CAD_CI_REPO", "").strip()
    if not value:
        raise RuntimeError("CAD_CI_ITEM_PATH is required")
    if not repo_value:
        raise RuntimeError("CAD_CI_REPO is required")

    item = Path(value).resolve()
    repo = Path(repo_value).resolve()
    try:
        return item.relative_to(repo).as_posix()
    except ValueError as exc:
        raise RuntimeError(
            f"CAD_CI_ITEM_PATH escapes CAD_CI_REPO: {item}"
        ) from exc


def main() -> int:
    """Run the selected model's contract tests with the dependency wheel."""

    run_contract_tests(item_path(), dependency_wheel())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
