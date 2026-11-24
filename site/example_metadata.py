"""Load and validate example-owned presentation metadata."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from scpf.model_metadata import MODEL_PURPOSES, validate_model_metadata


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_ROOT = ROOT / "examples"


def _text(value: Any, label: str) -> str:
    """Validate text used by the separate section-presentation config."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value.strip()


@dataclass(frozen=True)
class ExampleMetadata:
    """Validated human-facing metadata for one Forge example."""

    slug: str
    purpose: tuple[str, ...]
    section: str
    priority: int
    title: str
    tagline: str
    description: str
    parameters: str
    stages: tuple[str, ...]



SECTION_CONFIG = ROOT / "site" / "content" / "verification-sections.yml"


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
        raise ValueError(f"unknown example section: {section}") from exc


def load_example_metadata(path: Path) -> ExampleMetadata:
    """Load one example model.yml presentation contract."""

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


def discover_example_metadata(
    root: Path = EXAMPLES_ROOT,
    *,
    purpose: str | None = None,
) -> tuple[ExampleMetadata, ...]:
    """Discover canonical model metadata, optionally filtered by purpose."""

    if purpose is not None and purpose not in MODEL_PURPOSES:
        raise ValueError(f"unknown model purpose: {purpose}")

    rows = [
        load_example_metadata(path)
        for path in sorted(Path(root).glob("*/model.yml"))
    ]
    if purpose is not None:
        rows = [row for row in rows if purpose in row.purpose]
    if not rows:
        label = f" purpose {purpose!r}" if purpose is not None else ""
        raise ValueError(f"no model.yml files{label} found below {root}")

    slugs = [row.slug for row in rows]
    if len(slugs) != len(set(slugs)):
        raise ValueError("duplicate example slugs discovered")
    return tuple(rows)
