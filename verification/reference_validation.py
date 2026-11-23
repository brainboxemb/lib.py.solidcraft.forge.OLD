"""Run remaining Forge-owned independent reference implementations.

PythonSCAD and pyBOSL2 execution/presentation remain Forge-owned. Generic mesh
contract parsing and verification are delegated to lib.py.cad.verification.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import runpy
import time
import traceback
from typing import Any

from cad_verification import (
    VerificationFailure,
    load_geometry_contract,
    validate_mesh_geometry,
)

from verification.reference_preview import render_reference_preview


ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATIONS = ("pythonscad", "pybosl2")


def contract_path(slug: str) -> Path:
    """Return one required model-local geometry contract."""

    path = ROOT / "examples" / slug / "verification" / "reference_geometry.json"
    if not path.is_file():
        raise RuntimeError(f"{slug}: missing local reference contract: {path}")
    return path


def source_path(slug: str, implementation: str) -> Path:
    """Return one required Forge-owned reference source."""

    path = ROOT / "examples" / slug / implementation / "model.py"
    if not path.is_file():
        raise RuntimeError(
            f"{slug}: missing {implementation} reference source: {path}"
        )
    return path


def load_reference(path: Path):
    """Execute one reference source and return its exported model object."""

    namespace = runpy.run_path(str(path))
    if "model" not in namespace:
        raise RuntimeError(f"{path} must expose final geometry as model")
    return namespace["model"]


def export_reference(
    slug: str,
    implementation: str,
    target: Path,
) -> None:
    """Run one Forge-owned implementation and export one STL."""

    if implementation not in IMPLEMENTATIONS:
        raise RuntimeError(
            f"Forge reference runner does not own implementation: {implementation}"
        )
    source = source_path(slug, implementation)
    target.parent.mkdir(parents=True, exist_ok=True)
    model = load_reference(source)
    export = getattr(model, "export", None)
    if not callable(export):
        raise RuntimeError(
            f"{slug}/{implementation}: model has no export() method"
        )
    exported = export(str(target))
    if not target.is_file() and exported is not None:
        candidate = Path(exported)
        if candidate.is_file():
            target.write_bytes(candidate.read_bytes())

    if not target.is_file() or target.stat().st_size == 0:
        raise RuntimeError(
            f"{slug}/{implementation}: no non-empty STL was exported"
        )


def verify_exported(
    slug: str,
    implementation: str,
    output: Path,
) -> tuple[dict[str, Any], bool]:
    """Verify one exported STL and attach separate Forge presentation evidence."""

    target = output / slug / implementation
    stl = target / "model.stl"
    if not stl.is_file() or stl.stat().st_size == 0:
        raise RuntimeError(
            f"{slug}/{implementation}: no non-empty STL was exported"
        )
    try:
        evidence = validate_mesh_geometry(
            stl,
            load_geometry_contract(contract_path(slug)),
        )
    except VerificationFailure as exc:
        raise RuntimeError(
            f"{slug}/{implementation}: reference geometry failed: {exc}"
        ) from exc

    result = {
        "implementation": implementation,
        "status": "pass",
        "source": str(
            source_path(slug, implementation).relative_to(ROOT)
        ),
        "stl": str(stl.relative_to(output)),
        "geometry": evidence,
    }

    presentation_failed = False
    try:
        render_reference_preview(
            stl,
            target / "presentation",
            source_reference="model.stl",
        )
        result["presentation"] = {
            "status": "pass",
            "preview": "presentation/preview-iso.png",
            "metadata": "presentation/preview.json",
        }
    except Exception as exc:
        presentation_failed = True
        result["presentation"] = {
            "status": "fail",
            "error": "".join(
                traceback.format_exception_only(type(exc), exc)
            ).strip(),
        }

    (target / "verification.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result, presentation_failed


def write_failure(
    slug: str,
    implementation: str,
    output: Path,
    exc: Exception | str,
) -> dict[str, Any]:
    """Write structured per-case failure evidence and return it."""

    target = output / slug / implementation
    target.mkdir(parents=True, exist_ok=True)
    error = str(exc)
    try:
        source = str(source_path(slug, implementation).relative_to(ROOT))
    except Exception:
        source = None
    result = {
        "implementation": implementation,
        "status": "fail",
        "source": source,
        "error": error,
    }
    (target / "verification.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result


def verify_one(
    slug: str,
    implementation: str,
    output: Path,
) -> tuple[dict[str, Any], bool]:
    """Export, verify and render one remaining Forge-owned reference."""

    target = output / slug / implementation
    target.mkdir(parents=True, exist_ok=True)
    export_reference(slug, implementation, target / "model.stl")
    return verify_exported(slug, implementation, output)


def selected_implementations(value: str) -> tuple[str, ...]:
    """Parse and validate one Forge-owned implementation selection."""

    if value.strip().lower() == "all":
        return IMPLEMENTATIONS

    selected = tuple(
        item
        for item in value.replace(",", " ").split()
        if item
    )
    if not selected:
        raise RuntimeError("at least one implementation must be selected")

    unknown = sorted(set(selected) - set(IMPLEMENTATIONS))
    if unknown:
        raise RuntimeError(
            "Forge reference runner does not own implementation(s): "
            + ", ".join(unknown)
        )
    return selected


def selected_slugs(value: str) -> tuple[str, ...]:
    """Parse explicit cases or discover every reference contract."""

    if value.strip().lower() == "all":
        return tuple(
            path.parents[1].name
            for path in sorted(
                (ROOT / "examples").glob(
                    "*/verification/reference_geometry.json"
                )
            )
        )
    return tuple(
        item for item in value.replace(",", " ").split() if item
    )


def verify_batch(
    slugs: tuple[str, ...],
    implementations: tuple[str, ...],
    output: Path,
) -> tuple[list[dict[str, Any]], bool]:
    """Verify all selected cases, grouped by Forge-owned implementation."""

    by_slug: dict[str, list[dict[str, Any]]] = {
        slug: [] for slug in slugs
    }
    failed = False

    for implementation in implementations:
        implementation_started = time.perf_counter()
        for slug in slugs:
            try:
                result, presentation_failed = verify_one(
                    slug,
                    implementation,
                    output,
                )
                failed = failed or presentation_failed
            except Exception as exc:  # continue through the complete batch
                failed = True
                result = write_failure(
                    slug,
                    implementation,
                    output,
                    "".join(
                        traceback.format_exception_only(type(exc), exc)
                    ).strip(),
                )
            by_slug[slug].append(result)

        print(
            "REFERENCE BATCH TIMING "
            f"{implementation}_s={time.perf_counter() - implementation_started:.3f}",
            flush=True,
        )

    models = []
    for slug in slugs:
        rows = by_slug[slug]
        models.append(
            {
                "model": slug,
                "status": (
                    "pass"
                    if rows
                    and all(
                        row["status"] == "pass"
                        and row.get("presentation", {}).get("status") == "pass"
                        for row in rows
                    )
                    else "fail"
                ),
                "implementations": rows,
            }
        )
    return models, failed


def main() -> int:
    """Verify explicitly selected remaining Forge-owned references."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", required=True)
    parser.add_argument(
        "--implementations",
        default="all",
        help="all or a comma/space-separated Forge-owned implementation list",
    )
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--source-sha", required=True)
    args = parser.parse_args()

    slugs = selected_slugs(args.cases)
    if not slugs:
        raise RuntimeError("at least one model must be selected")
    implementations = selected_implementations(args.implementations)

    args.out.mkdir(parents=True, exist_ok=True)
    models, failed = verify_batch(slugs, implementations, args.out)
    report = {
        "schema": 1,
        "source_sha": args.source_sha,
        "status": "fail" if failed else "pass",
        "models": models,
    }
    (args.out / "verification.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        "Forge-owned reference verification: "
        + ", ".join(
            row["model"] + "=" + row["status"] for row in models
        ),
        flush=True,
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
