"""Resolve repository-backed Forge test fixtures by stable slug."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE_ROOTS = (
    ROOT / "examples",
    ROOT / "verification" / "cases",
    ROOT / "verification" / "regressions",
)


def fixture_root(slug: str) -> Path:
    """Return the unique repository fixture root for one stable model slug."""

    matches = tuple(root / slug for root in FIXTURE_ROOTS if (root / slug).is_dir())
    if len(matches) != 1:
        raise AssertionError(
            f"{slug}: expected exactly one repository fixture root, found "
            + ", ".join(path.as_posix() for path in matches)
        )
    return matches[0]


def fixture_path(slug: str, *parts: str) -> Path:
    """Return a path below the unique repository fixture root."""

    return fixture_root(slug).joinpath(*parts)


def public_verification_roots() -> tuple[Path, ...]:
    """Return public Verification case roots in stable slug order."""

    root = ROOT / "verification" / "cases"
    return tuple(
        path for path in sorted(root.iterdir())
        if path.is_dir()
    )
