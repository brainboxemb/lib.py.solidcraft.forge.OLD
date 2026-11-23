#!/usr/bin/env python3
"""Run remaining Forge-owned PythonSCAD/pyBOSL2 references and diagrams."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

import yaml

from forge_example import dependency_wheel


ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATIONS = ("pythonscad", "pybosl2")


def output_root() -> Path:
    """Return this CAD-CI item's output root."""

    value = os.environ.get("CAD_CI_OUTPUT", "").strip()
    if not value:
        raise RuntimeError("CAD_CI_OUTPUT is required")
    path = Path(value).resolve()
    path.mkdir(parents=True, exist_ok=True)
    return path


def runtime_image() -> str:
    """Return the immutable heavy reference runtime image."""

    value = os.environ.get("REFERENCE_RUNTIME_IMAGE", "").strip()
    if not value:
        raise RuntimeError("REFERENCE_RUNTIME_IMAGE is required")
    return value


def source_sha() -> str:
    """Return the exact source commit under verification."""

    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        text=True,
    ).strip()


def processed_reference_slugs() -> tuple[str, ...]:
    """Return process:true models with the remaining Forge-owned reference set."""

    slugs: list[str] = []
    for ci_path in sorted((ROOT / "examples").glob("*/ci.yml")):
        config = yaml.safe_load(ci_path.read_text(encoding="utf-8")) or {}
        if config.get("process", True) is False:
            continue
        model_root = ci_path.parent
        if not (
            model_root / "verification" / "reference_geometry.json"
        ).is_file():
            continue
        missing = [
            implementation
            for implementation in IMPLEMENTATIONS
            if not (model_root / implementation / "ci.yml").is_file()
            or not (model_root / implementation / "model.py").is_file()
        ]
        if missing:
            raise RuntimeError(
                f"{model_root.name}: incomplete reference set: "
                + ", ".join(missing)
            )
        slugs.append(model_root.name)

    if not slugs:
        raise RuntimeError("no processed reference models found")
    return tuple(slugs)


def run_inside_runtime(cases: str, commit: str) -> int:
    """Run preview tests, references and CADCraft diagrams in one runtime."""

    for name in ("references", "diagrams"):
        path = Path("/output") / name
        if path.exists():
            shutil.rmtree(path)

    preview_tests = subprocess.run(
        [
            "python",
            "/workspace/verification/tests/test_reference_preview.py",
        ],
        cwd="/workspace",
        check=False,
    )

    reference = subprocess.run(
        [
            "python",
            "/workspace/verification/reference_validation.py",
            "--cases",
            cases,
            "--implementations",
            ",".join(IMPLEMENTATIONS),
            "--out",
            "/output/references",
            "--source-sha",
            commit,
        ],
        cwd="/workspace",
        check=False,
    )

    diagrams = subprocess.run(
        [
            "python",
            "/workspace/scripts/build_diagrams.py",
            "--out",
            "/output/diagrams",
        ],
        cwd="/workspace",
        check=False,
    )

    return (
        0
        if (
            preview_tests.returncode == 0
            and reference.returncode == 0
            and diagrams.returncode == 0
        )
        else 1
    )


def build_item_projections(output: Path, slugs: tuple[str, ...]) -> int:
    """Build every child-owned reference output once from the aggregate report."""

    references = output / "references"
    report_path = references / "verification.json"
    if not report_path.is_file():
        raise RuntimeError(f"missing reference batch report: {report_path}")
    report = json.loads(report_path.read_text(encoding="utf-8"))

    items = output / "items"
    if items.exists():
        shutil.rmtree(items)
    items.mkdir(parents=True)

    failed = False
    for slug in slugs:
        model = next(
            (
                row
                for row in report.get("models", [])
                if row.get("model") == slug
            ),
            None,
        )
        if model is None:
            raise RuntimeError(f"missing batch report row for {slug}")

        for implementation in IMPLEMENTATIONS:
            implementation_row = next(
                (
                    row
                    for row in model.get("implementations", [])
                    if row.get("implementation") == implementation
                ),
                None,
            )
            if implementation_row is None:
                raise RuntimeError(
                    f"missing batch report row for {slug}/{implementation}"
                )

            source = references / slug / implementation
            if not source.is_dir():
                raise RuntimeError(
                    f"missing reference batch result: {source}"
                )

            destination = (
                items
                / "examples"
                / slug
                / implementation
                / "references"
            )
            case_destination = destination / slug / implementation
            case_destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(
                source,
                case_destination,
                dirs_exist_ok=True,
            )

            presentation_status = implementation_row.get(
                "presentation",
                {},
            ).get("status")
            child_status = (
                "pass"
                if (
                    implementation_row.get("status") == "pass"
                    and presentation_status == "pass"
                )
                else "fail"
            )
            child_report = {
                "schema": report.get("schema", 1),
                "source_sha": report.get("source_sha"),
                "status": child_status,
                "models": [
                    {
                        "model": slug,
                        "status": child_status,
                        "implementations": [implementation_row],
                    }
                ],
            }
            destination.mkdir(parents=True, exist_ok=True)
            (destination / "verification.json").write_text(
                json.dumps(
                    child_report,
                    indent=2,
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )
            failed = failed or child_status != "pass"

    return 1 if failed else 0


def run_batch() -> int:
    """Run all active heavy-reference work and build child projection outputs."""

    output = output_root()
    items = output / "items"
    if items.exists():
        shutil.rmtree(items)

    wheel = dependency_wheel(
        "cad-ci-verification-package",
        "brainboxemb_cad_verification_lib-*.whl",
    )
    image = runtime_image()
    slugs = processed_reference_slugs()

    batch_started = time.perf_counter()
    pull_started = time.perf_counter()
    subprocess.run(["docker", "pull", image], check=True)
    print(
        "REFERENCE BATCH TIMING "
        f"image_pull_s={time.perf_counter() - pull_started:.3f}",
        flush=True,
    )

    container_started = time.perf_counter()
    completed = subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "--pull=never",
            "-v",
            f"{ROOT}:/workspace:ro",
            "-v",
            f"{output}:/output",
            "-v",
            f"{wheel.parent}:/cad-verification:ro",
            "-w",
            "/workspace",
            "-e",
            (
                "PYTHONPATH="
                f"/cad-verification/{wheel.name}:"
                "/workspace/scpf:/workspace"
            ),
            image,
            "python",
            "/workspace/scripts/reference_verification_batch.py",
            "inside",
            "--cases",
            ",".join(slugs),
            "--source-sha",
            source_sha(),
        ],
        cwd=ROOT,
        check=False,
    )
    print(
        "REFERENCE BATCH TIMING "
        f"container_process_s={time.perf_counter() - container_started:.3f}",
        flush=True,
    )

    if completed.returncode != 0:
        print(
            "REFERENCE BATCH TIMING "
            f"total_s={time.perf_counter() - batch_started:.3f}",
            flush=True,
        )
        return completed.returncode

    projection_started = time.perf_counter()
    projection_status = build_item_projections(output, slugs)
    print(
        "REFERENCE BATCH TIMING "
        f"projection_s={time.perf_counter() - projection_started:.3f}",
        flush=True,
    )
    print(
        "REFERENCE BATCH TIMING "
        f"total_s={time.perf_counter() - batch_started:.3f}",
        flush=True,
    )
    return projection_status


def main() -> int:
    """Dispatch batch production or in-runtime reference work."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "operation",
        nargs="?",
        choices=("batch", "inside"),
        default="batch",
    )
    parser.add_argument("--cases")
    parser.add_argument("--source-sha")
    args = parser.parse_args()

    if args.operation == "inside":
        if not args.cases or not args.source_sha:
            parser.error("inside requires --cases and --source-sha")
        return run_inside_runtime(args.cases, args.source_sha)

    if args.cases is not None or args.source_sha is not None:
        parser.error("--cases/--source-sha require inside")
    return run_batch()


if __name__ == "__main__":
    raise SystemExit(main())
