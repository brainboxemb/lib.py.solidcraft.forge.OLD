#!/usr/bin/env python3
"""Publish one already-verified Forge release from durable repository evidence."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.release.validate_release import FULL_SHA, SEMVER, validate


def run(
    args: list[str], *, capture: bool = False, check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Run one repository publication command."""
    return subprocess.run(
        args,
        cwd=ROOT,
        check=check,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )


def output(args: list[str]) -> str:
    """Run a command and return stripped stdout."""
    return run(args, capture=True).stdout.strip()


def fetch_release_inputs() -> None:
    """Fetch exact source/evidence refs and release tags."""
    run(
        [
            "git",
            "fetch",
            "--no-tags",
            "origin",
            "+refs/heads/main:refs/remotes/origin/main",
            "+refs/heads/build:refs/remotes/origin/build",
            "+refs/heads/gh-pages:refs/remotes/origin/gh-pages",
        ]
    )
    run(["git", "fetch", "origin", "--tags"])


def tag_target(tag: str) -> str | None:
    """Return the commit resolved by tag, or None when the tag is absent."""
    completed = run(
        ["git", "rev-list", "-n", "1", tag],
        capture=True,
        check=False,
    )
    if completed.returncode != 0:
        return None
    value = completed.stdout.strip()
    return value or None


def verify_existing_tag(tag: str, target_sha: str) -> bool:
    """Validate an existing tag; return False only when the tag is absent."""
    current = tag_target(tag)
    if current is None:
        return False
    object_type = output(["git", "cat-file", "-t", tag])
    if object_type != "tag":
        raise SystemExit(f"{tag} exists but is not an annotated tag")
    if current != target_sha:
        raise SystemExit(f"{tag} points to {current}, expected {target_sha}")
    return True


def release_url(repository: str, tag: str) -> str | None:
    """Return an existing GitHub Release URL, or None when absent."""
    completed = run(
        [
            "gh",
            "release",
            "view",
            tag,
            "--repo",
            repository,
            "--json",
            "url",
            "--jq",
            ".url",
        ],
        capture=True,
        check=False,
    )
    if completed.returncode != 0:
        return None
    value = completed.stdout.strip()
    return value or None


def create_tag(tag: str, target_sha: str) -> None:
    """Create and push one annotated immutable release tag."""
    run(["git", "config", "user.name", "github-actions[bot]"])
    run(
        [
            "git",
            "config",
            "user.email",
            "41898282+github-actions[bot]@users.noreply.github.com",
        ]
    )
    run(["git", "tag", "-a", tag, target_sha, "-m", f"SCPF {tag}"])
    run(["git", "push", "origin", f"refs/tags/{tag}"])


def publish(*, repository: str, version: str, target_sha: str) -> tuple[str, str]:
    """Validate and publish one exact version/SHA pair."""
    if SEMVER.fullmatch(version) is None:
        raise SystemExit("version must be plain SemVer, for example 0.11.0")
    if FULL_SHA.fullmatch(target_sha) is None:
        raise SystemExit("target SHA must contain exactly 40 lowercase hex characters")

    tag = f"v{version}"
    fetch_release_inputs()

    with tempfile.TemporaryDirectory() as temp:
        notes = Path(temp) / "release-notes.md"
        validate(version, target_sha, notes)

        existing_release = release_url(repository, tag)
        tag_exists = verify_existing_tag(tag, target_sha)
        if existing_release is not None:
            if not tag_exists:
                raise SystemExit(
                    f"GitHub Release {tag} exists without the expected annotated tag"
                )
            return tag, existing_release

        if not tag_exists:
            create_tag(tag, target_sha)

        if not verify_existing_tag(tag, target_sha):
            raise SystemExit(f"failed to create {tag}")

        run(
            [
                "gh",
                "release",
                "create",
                tag,
                "--repo",
                repository,
                "--verify-tag",
                "--title",
                f"SCPF {tag}",
                "--notes-file",
                str(notes),
            ]
        )

        published = release_url(repository, tag)
        if published is None:
            raise SystemExit(f"GitHub Release {tag} was not created")
        if not verify_existing_tag(tag, target_sha):
            raise SystemExit(f"{tag} no longer resolves to {target_sha}")
        return tag, published


def write_github_output(path: Path | None, *, tag: str, url: str) -> None:
    if path is None:
        return
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"tag={tag}\n")
        handle.write(f"url={url}\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--target-sha", required=True)
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args()

    tag, url = publish(
        repository=args.repository,
        version=args.version,
        target_sha=args.target_sha,
    )
    write_github_output(args.github_output, tag=tag, url=url)
    print(f"Published and verified {tag} at {args.target_sha}: {url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
