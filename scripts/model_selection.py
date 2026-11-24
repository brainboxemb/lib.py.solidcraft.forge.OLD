"""Select Forge model roles from canonical model.yml metadata."""

from __future__ import annotations

from pathlib import Path
import sys

import yaml


def example_slugs(package: Path, root: Path) -> tuple[str, ...]:
    """Return deterministic model slugs whose canonical purpose contains example."""

    package_text = str(package)
    if package_text not in sys.path:
        sys.path.insert(0, package_text)

    from scpf.model_metadata import validate_model_metadata

    slugs = []
    for path in sorted((root / "examples").glob("*/model.yml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        metadata = validate_model_metadata(data, label=str(path))
        if "example" in metadata.purpose:
            slugs.append(path.parent.name)

    if not slugs:
        raise RuntimeError("canonical model metadata selects no Example models")
    return tuple(slugs)
