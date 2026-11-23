"""Validate one exact Forge release candidate from durable repository evidence."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import tomllib
from pathlib import Path

SEMVER = re.compile(r"\d+\.\d+\.\d+")
FULL_SHA = re.compile(r"[0-9a-f]{40}")
BLOCKERS_PATH = "docs/background/design/release-blockers.txt"
BUILD_MANIFEST_PATH = "main/build.json"
PAGES_PROVENANCE_PATH = "provenance.json"


def git(*args: str) -> str:
    """Run git and return stripped stdout."""
    return subprocess.check_output(["git", *args], text=True).strip()


def read_at(ref: str, path: str) -> str:
    """Read one UTF-8 repository file from a Git ref."""
    return git("show", f"{ref}:{path}")


def active_blockers(text: str) -> tuple[str, ...]:
    """Return non-comment release-blocker lines."""
    return tuple(
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    )


def release_notes(changelog: str, version: str) -> str:
    """Extract the dated changelog section for one exact version."""
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

    next_heading = re.compile(r"^## \[", re.MULTILINE).search(changelog, match.end())
    end = next_heading.start() if next_heading else len(changelog)
    notes = changelog[match.start():end].strip()
    if not re.search(r"^### ", notes, re.MULTILINE):
        raise SystemExit(f"CHANGELOG.md [{version}] section has no release content")
    return notes + "\n"


def validate_durable_evidence(target_sha: str) -> None:
    """Require durable main build and stable Pages evidence for target_sha."""
    build = json.loads(read_at("origin/build", BUILD_MANIFEST_PATH))
    if build.get("scope") != "main":
        raise SystemExit("build/main manifest is not scope=main")
    if build.get("source_commit") != target_sha:
        raise SystemExit(
            "build/main source_commit does not match release target: "
            f"{build.get('source_commit')!r}"
        )

    release_item = build.get("items", {}).get("ci/forge-release")
    if not isinstance(release_item, dict):
        raise SystemExit("build/main has no ci/forge-release evidence")
    if release_item.get("source_commit") != target_sha:
        raise SystemExit(
            "forge-release evidence does not match release target: "
            f"{release_item.get('source_commit')!r}"
        )
    if release_item.get("final_step") != "tool_verify":
        raise SystemExit("forge-release evidence did not finish at tool_verify")

    pages = json.loads(read_at("origin/gh-pages", PAGES_PROVENANCE_PATH))
    if pages.get("source_commit") != target_sha:
        raise SystemExit(
            "stable Pages source_commit does not match release target: "
            f"{pages.get('source_commit')!r}"
        )
    if pages.get("build_manifest_source_commit") != target_sha:
        raise SystemExit(
            "stable Pages build-manifest source does not match release target: "
            f"{pages.get('build_manifest_source_commit')!r}"
        )


def validate(version: str, target_sha: str, notes_out: Path) -> str:
    """Validate release metadata/evidence and write extracted release notes."""
    if SEMVER.fullmatch(version) is None:
        raise SystemExit("version must be plain SemVer, for example 0.11.0")
    if FULL_SHA.fullmatch(target_sha) is None:
        raise SystemExit("target_sha must be a full 40-character commit SHA")

    main_sha = git("rev-parse", "origin/main")
    if target_sha != main_sha:
        raise SystemExit(
            f"release target must equal current main HEAD: {main_sha}"
        )

    blockers = active_blockers(read_at(target_sha, BLOCKERS_PATH))
    if blockers:
        detail = "\n".join(f"- {blocker}" for blocker in blockers)
        raise SystemExit("release blocked by foundational Forge issue(s):\n" + detail)

    pyproject = tomllib.loads(read_at(target_sha, "scpf/pyproject.toml"))
    package_version = pyproject["project"]["version"]
    if package_version != version:
        raise SystemExit(
            f"package version mismatch: expected {version}, found {package_version}"
        )

    changelog = read_at(target_sha, "CHANGELOG.md")
    notes_out.write_text(release_notes(changelog, version), encoding="utf-8")

    version_source = read_at(target_sha, "scpf/scpf/version.py")
    solidcraft = re.search(
        r'^TESTED_SOLIDCRAFT_VERSION = "([^"]+)"$',
        version_source,
        re.MULTILINE,
    )
    if solidcraft is None:
        raise SystemExit("cannot read TESTED_SOLIDCRAFT_VERSION")

    validate_durable_evidence(target_sha)
    return solidcraft.group(1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    parser.add_argument("--target-sha", required=True)
    parser.add_argument(
        "--notes-out", type=Path, default=Path("release-notes.md")
    )
    args = parser.parse_args()

    solidcraft = validate(args.version, args.target_sha, args.notes_out)
    print(f"SCPF {args.version}; qualified SolidCraft {solidcraft}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
