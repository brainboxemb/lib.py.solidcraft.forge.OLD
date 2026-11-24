"""Load and validate public Example and Verification catalog metadata."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import yaml

from scpf.model_metadata import validate_model_metadata


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_ROOT = ROOT / "examples"
VERIFICATION_CASES_ROOT = ROOT / "verification" / "cases"
SECTION_CONFIG = ROOT / "site" / "content" / "verification-sections.yml"


def _text(value: Any, label: str) -> str:
    """Validate text used by the separate section-presentation config."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value.strip()


@dataclass(frozen=True)
class ExampleMetadata:
    """Validated human-facing metadata for one public catalog item."""

    slug: str
    section: str
    priority: int
    title: str
    tagline: str
    description: str
    parameters: str
    stages: tuple[str, ...]
    source_root: Path
    source_path: str
    public_example: bool
    public_verification: bool


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
        raise ValueError(f"unknown verification section: {section}") from exc


def _relative_source_path(root: Path) -> str:
    """Return one repository-relative catalog source path."""

    root = Path(root).resolve()
    try:
        return root.relative_to(ROOT.resolve()).as_posix()
    except ValueError as exc:
        raise ValueError(f"catalog source is outside repository: {root}") from exc


def _load_example_roles(example_root: Path) -> tuple[bool, bool]:
    """Load explicit public roles for one teaching example."""

    path = Path(example_root) / "catalog.yml"
    if not path.is_file():
        raise ValueError(
            f"{example_root.name}: teaching example requires catalog.yml"
        )
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema") != 1:
        raise ValueError(f"{example_root.name}: catalog.yml must use schema 1")
    public_example = data.get("public_example")
    public_verification = data.get("public_verification")
    if not isinstance(public_example, bool):
        raise ValueError(
            f"{example_root.name}: public_example must be boolean"
        )
    if not isinstance(public_verification, bool):
        raise ValueError(
            f"{example_root.name}: public_verification must be boolean"
        )
    if not public_example and not public_verification:
        raise ValueError(
            f"{example_root.name}: catalog.yml must expose at least one public role"
        )
    return public_example, public_verification


def load_example_metadata(
    path: Path,
    *,
    public_example: bool,
    public_verification: bool,
) -> ExampleMetadata:
    """Load one model.yml presentation contract with explicit catalog roles."""

    path = Path(path)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: model.yml must contain one mapping")

    slug = path.parent.name
    metadata = validate_model_metadata(data, label=f"{slug}.model.yml")
    return ExampleMetadata(
        slug=slug,
        section=metadata.section,
        priority=metadata.priority,
        title=metadata.title,
        tagline=metadata.tagline,
        description=metadata.description,
        parameters=metadata.parameters,
        stages=metadata.stages,
        source_root=path.parent,
        source_path=_relative_source_path(path.parent),
        public_example=public_example,
        public_verification=public_verification,
    )


def _validate_unique(
    rows: Iterable[ExampleMetadata],
    *,
    label: str,
) -> tuple[ExampleMetadata, ...]:
    """Return stable catalog rows while rejecting duplicate public slugs."""

    result = tuple(rows)
    if not result:
        raise ValueError(f"no {label} catalog entries discovered")
    slugs = [row.slug for row in result]
    duplicates = sorted({slug for slug in slugs if slugs.count(slug) > 1})
    if duplicates:
        raise ValueError(
            f"duplicate {label} slugs discovered: " + ", ".join(duplicates)
        )
    return result


def _teaching_rows(root: Path = EXAMPLES_ROOT) -> tuple[ExampleMetadata, ...]:
    """Load all explicitly catalogued teaching roots."""

    rows = []
    for path in sorted(Path(root).glob("*/model.yml")):
        public_example, public_verification = _load_example_roles(path.parent)
        rows.append(
            load_example_metadata(
                path,
                public_example=public_example,
                public_verification=public_verification,
            )
        )
    return tuple(rows)


def discover_example_metadata(
    root: Path = EXAMPLES_ROOT,
) -> tuple[ExampleMetadata, ...]:
    """Discover the deliberately small public teaching-example catalog."""

    return _validate_unique(
        (
            row
            for row in _teaching_rows(root)
            if row.public_example
        ),
        label="Example",
    )


def discover_verification_metadata(
    cases_root: Path = VERIFICATION_CASES_ROOT,
    examples_root: Path = EXAMPLES_ROOT,
) -> tuple[ExampleMetadata, ...]:
    """Discover the independent public Verification capability catalog."""

    rows = [
        load_example_metadata(
            path,
            public_example=False,
            public_verification=True,
        )
        for path in sorted(Path(cases_root).glob("*/model.yml"))
    ]
    rows.extend(
        row
        for row in _teaching_rows(examples_root)
        if row.public_verification
    )
    rows.sort(key=lambda row: row.slug)
    return _validate_unique(rows, label="Verification")
