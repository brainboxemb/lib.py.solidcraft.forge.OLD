"""Forge-specific checks used by the shared CAD release workflow."""

from __future__ import annotations

import argparse
import re
import tomllib
from pathlib import Path

BLOCKERS_PATH = Path("docs/background/design/release-blockers.txt")


def active_blockers(text: str) -> tuple[str, ...]:
    """Return non-comment Forge release-blocker lines."""

    return tuple(
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    )


def release_notes(changelog: str, version: str) -> str:
    """Extract the dated changelog section for one exact Forge version."""

    unreleased = changelog.find("## [Unreleased]")
    if unreleased < 0:
        raise SystemExit("CHANGELOG.md has no [Unreleased] section")

    heading = re.compile(
        rf"^## \[{re.escape(version)}\] - \d{{4}}-\d{{2}}-\d{{2}}$",
        re.MULTILINE,
    )
    match = heading.search(changelog)
    if match is None:
        raise SystemExit(f"CHANGELOG.md has no dated [{version}] section")
    if match.start() < unreleased:
        raise SystemExit(f"[{version}] must follow the [Unreleased] section")

    next_heading = re.compile(r"^## \[", re.MULTILINE).search(
        changelog, match.end()
    )
    end = next_heading.start() if next_heading else len(changelog)
    notes = changelog[match.start():end].strip()
    if not re.search(r"^### ", notes, re.MULTILINE):
        raise SystemExit(
            f"CHANGELOG.md [{version}] section has no release content"
        )
    return notes + "\n"


def validate(
    version: str,
    target_sha: str,
    notes_out: Path,
    *,
    root: Path = Path("."),
) -> str:
    """Check Forge-owned release metadata in the exact shared-workflow checkout."""

    _ = target_sha  # Exact source selection is owned by the shared release flow.

    blockers = active_blockers(
        (root / BLOCKERS_PATH).read_text(encoding="utf-8")
    )
    if blockers:
        detail = "\n".join(f"- {blocker}" for blocker in blockers)
        raise SystemExit(
            "release blocked by foundational Forge issue(s):\n" + detail
        )

    pyproject = tomllib.loads(
        (root / "scpf/pyproject.toml").read_text(encoding="utf-8")
    )
    package_version = pyproject["project"]["version"]
    if package_version != version:
        raise SystemExit(
            f"package version mismatch: expected {version}, "
            f"found {package_version}"
        )

    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    notes_out.write_text(
        release_notes(changelog, version),
        encoding="utf-8",
    )

    version_source = (root / "scpf/scpf/version.py").read_text(
        encoding="utf-8"
    )
    solidcraft = re.search(
        r'^TESTED_SOLIDCRAFT_VERSION = "([^"]+)"$',
        version_source,
        re.MULTILINE,
    )
    if solidcraft is None:
        raise SystemExit("cannot read TESTED_SOLIDCRAFT_VERSION")
    return solidcraft.group(1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    parser.add_argument("--target-sha", required=True)
    parser.add_argument(
        "--notes-out",
        type=Path,
        default=Path("release-notes.md"),
    )
    args = parser.parse_args()

    solidcraft = validate(args.version, args.target_sha, args.notes_out)
    print(f"SCPF {args.version}; qualified SolidCraft {solidcraft}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
