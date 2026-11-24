"""Load and validate purpose-based Forge model presentation metadata."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from scpf.model_metadata import validate_model_metadata


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_ROOT = ROOT / "examples"
SECTION_CONFIG = ROOT / "site" / "content" / "verification-sections.yml"


def _text(value: Any, label: str) -> str:
    """Validate text used by the separate section-presentation config."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value.strip()


@dataclass(frozen=True)
class ExampleMetadata:
    """Validated human-facing metadata for one Forge model catalog item."""

    slug: str
    purpose: frozenset[str]
    section: str
    priority: int
    title: str
    tagline: str
    description: str
    parameters: str
    stages: tuple[str, ...]


def load_section_presentation(
    path: Path = SECTION_CONFIG,
) -> dict[str, tuple[int, str, str]]:
    """Load declarative verification section priorities and labels."""

    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema") != 1:
        raise ValueError("verification section config must use schema 1")
    sections = data.get("sections")
    if not isinstance(sections, dict) or not sections:
        raise ValueError("verification section config requires sections")

    result = {}
    priorities = set()
    for slug, row in sections.items():
        if not isinstance(slug, str) or not slug.strip():
            raise ValueError("verification section slug must be text")
        if not isinstance(row, dict):
            raise ValueError(f"{slug}: section config must be a mapping")
        priority = row.get("priority")
        label = row.get("label")
        description = row.get("description")
        if not isinstance(priority, int) or priority < 1:
            raise ValueError(f"{slug}.priority must be a positive integer")
        if priority in priorities:
            raise ValueError(
                f"duplicate verification section priority: {priority}"
            )
        priorities.add(priority)
        result[slug] = (
            priority,
            _text(label, f"{slug}.label"),
            _text(description, f"{slug}.description"),
        )
    return result


def section_presentation(section: str) -> tuple[int, str, str]:
    """Return configured public priority, label and description for one section slug."""

    sections = load_section_presentation()
    try:
        return sections[section]
    except KeyError as exc:
        raise ValueError(f"unknown model section: {section}") from exc


def load_example_metadata(path: Path) -> ExampleMetadata:
    """Load one canonical model.yml presentation contract."""

    path = Path(path)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: model.yml must contain one mapping")

    slug = path.parent.name
    metadata = validate_model_metadata(data, label=f"{slug}.model.yml")
    return ExampleMetadata(
        slug=slug,
        purpose=metadata.purpose,
        section=metadata.section,
        priority=metadata.priority,
        title=metadata.title,
        tagline=metadata.tagline,
        description=metadata.description,
        parameters=metadata.parameters,
        stages=metadata.stages,
    )


def discover_model_metadata(
    root: Path = EXAMPLES_ROOT,
) -> tuple[ExampleMetadata, ...]:
    """Discover every model that owns canonical model.yml metadata."""

    rows = [
        load_example_metadata(path)
        for path in sorted(Path(root).glob("*/model.yml"))
    ]
    if not rows:
        raise ValueError(f"no model.yml files found below {root}")

    slugs = [row.slug for row in rows]
    if len(slugs) != len(set(slugs)):
        raise ValueError("duplicate model slugs discovered")
    return tuple(rows)


def _purpose_rows(
    purpose: str,
    root: Path,
) -> tuple[ExampleMetadata, ...]:
    rows = tuple(
        row
        for row in discover_model_metadata(root)
        if purpose in row.purpose
    )
    if not rows:
        raise ValueError(f"no {purpose} models discovered below {root}")
    return rows


def discover_example_metadata(
    root: Path = EXAMPLES_ROOT,
) -> tuple[ExampleMetadata, ...]:
    """Discover the curated public teaching Example catalog."""

    return _purpose_rows("example", Path(root))


def discover_verification_metadata(
    root: Path = EXAMPLES_ROOT,
) -> tuple[ExampleMetadata, ...]:
    """Discover the broader public Verification capability catalog."""

    return _purpose_rows("verification", Path(root))
