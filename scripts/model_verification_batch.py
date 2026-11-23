#!/usr/bin/env python3
"""Run declarative SolidCraft verification as one shared runtime batch."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import traceback
import time

import yaml

from forge_example import (
    compile_commands,
    dependency_wheel,
    verification_wheel,
    write_commands,
)


ROOT = Path(__file__).resolve().parents[1]

def output_root() -> Path:
    """Return this CAD-CI item's output root."""

    value = os.environ.get("CAD_CI_OUTPUT", "").strip()
    if not value:
        raise RuntimeError("CAD_CI_OUTPUT is required")
    path = Path(value).resolve()
    path.mkdir(parents=True, exist_ok=True)
    return path


def runtime_image() -> str:
    """Return the immutable SolidCraft runtime image."""

    value = os.environ.get("FORGE_RUNTIME_IMAGE", "").strip()
    if not value:
        raise RuntimeError("FORGE_RUNTIME_IMAGE is required")
    return value


def source_sha() -> str:
    """Return the exact source commit under verification."""

    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        text=True,
    ).strip()


def processed_declarative_slugs() -> tuple[str, ...]:
    """Return process:true models that own declarative verification data."""

    slugs: list[str] = []
    for verify in sorted((ROOT / "examples").glob("*/verification/verify.py")):
        model_root = verify.parents[1]
        ci_path = model_root / "ci.yml"
        if not ci_path.is_file():
            continue
        config = yaml.safe_load(ci_path.read_text(encoding="utf-8")) or {}
        if config.get("process", True) is False:
            continue
        slugs.append(model_root.name)
    if not slugs:
        raise RuntimeError("no processed declarative models found")
    return tuple(slugs)


def active_declarative_slugs(
    processed: tuple[str, ...] | None = None,
) -> tuple[str, ...]:
    """Return the released CAD-CI active direct model dependents."""

    raw = os.environ.get("CAD_CI_ACTIVE_DEPENDENTS_JSON")
    if raw is None:
        raise RuntimeError(
            "CAD_CI_ACTIVE_DEPENDENTS_JSON is required for the model batch"
        )
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "CAD_CI_ACTIVE_DEPENDENTS_JSON must be valid JSON"
        ) from exc
    if (
        not isinstance(value, list)
        or any(not isinstance(item, str) or not item for item in value)
        or len(set(value)) != len(value)
    ):
        raise RuntimeError(
            "CAD_CI_ACTIVE_DEPENDENTS_JSON must be a unique string list"
        )

    processed_slugs = (
        processed_declarative_slugs()
        if processed is None
        else tuple(processed)
    )
    allowed = set(processed_slugs)
    unknown = [item for item in value if item not in allowed]
    if unknown:
        raise RuntimeError(
            "unexpected model batch direct dependent(s): "
            + ", ".join(unknown)
        )
    return tuple(value)


def write_manifest(
    batch_root: Path,
    wheel: Path,
    slugs: tuple[str, ...],
) -> Path:
    """Compile the selected model subset and write one runtime manifest."""

    rows = []
    for slug in slugs:
        case_root = batch_root / "examples" / slug
        case_root.mkdir(parents=True, exist_ok=True)
        command_path = case_root / "solidcraft.json"
        try:
            write_commands(compile_commands(slug, wheel), command_path)
            compile_error = None
        except Exception as exc:  # compile all models before failing the batch
            compile_error = "".join(
                traceback.format_exception_only(type(exc), exc)
            ).strip()
            print(
                f"{slug} Forge compile: error: {compile_error}",
                flush=True,
            )
        rows.append(
            {
                "slug": slug,
                "input": f"/output/items/examples/{slug}/solidcraft.json",
                "output": f"/output/items/examples/{slug}/model_verify",
                "compile_error": compile_error,
            }
        )

    manifest = batch_root / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "schema": 1,
                "source_sha": source_sha(),
                "models": rows,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return manifest


def run_host_batch() -> int:
    """Compile the selected cases, then verify them in one SolidCraft container."""

    output = output_root()
    batch_root = output / "items"
    if batch_root.exists():
        shutil.rmtree(batch_root)
    batch_root.mkdir(parents=True)

    slugs = active_declarative_slugs()
    print(
        "FORGE BATCH selected models: "
        + (", ".join(slugs) if slugs else "none"),
        flush=True,
    )
    if not slugs:
        return 0

    forge_wheel = dependency_wheel("forge-package", "scpf-*.whl")
    verification_package = verification_wheel()
    batch_started = time.perf_counter()
    compile_started = time.perf_counter()
    manifest = write_manifest(batch_root, forge_wheel, slugs)
    print(
        "FORGE BATCH TIMING "
        f"compile_all_s={time.perf_counter() - compile_started:.3f}",
        flush=True,
    )
    image = runtime_image()

    pull_started = time.perf_counter()
    subprocess.run(["docker", "pull", image], check=True)
    print(
        "FORGE BATCH TIMING "
        f"image_pull_s={time.perf_counter() - pull_started:.3f}",
        flush=True,
    )

    container_forge_wheel = f"/forge-package/{forge_wheel.name}"
    container_verification_wheel = (
        f"/cad-verification/{verification_package.name}"
    )
    container_started = time.perf_counter()
    completed = subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "--pull=never",
            "-e",
            (
                "PYTHONPATH="
                f"{container_verification_wheel}:{container_forge_wheel}"
            ),
            "-e",
            "SOLIDCRAFT_GPU=cpu",
            "-v",
            f"{ROOT}:/workspace:ro",
            "-v",
            f"{output}:/output",
            "-v",
            f"{forge_wheel.parent}:/forge-package:ro",
            "-v",
            f"{verification_package.parent}:/cad-verification:ro",
            "-w",
            "/workspace",
            image,
            "python",
            "/workspace/scripts/model_verification_batch.py",
            "--inside-runtime",
            "--manifest",
            "/output/items/manifest.json",
        ],
        cwd=ROOT,
        check=False,
    )
    print(
        "FORGE BATCH TIMING "
        f"container_process_s={time.perf_counter() - container_started:.3f}",
        flush=True,
    )
    print(
        "FORGE BATCH TIMING "
        f"total_s={time.perf_counter() - batch_started:.3f}",
        flush=True,
    )
    return completed.returncode


def run_inside_runtime(manifest_path: Path) -> int:
    """Process every model, retaining failures until the complete list is done."""

    from model_verify_declarative import run_inside_runtime as verify_one

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    rows = manifest.get("models")
    if not isinstance(rows, list) or not rows:
        raise RuntimeError("model verification batch manifest has no models")

    results = []
    failed = False
    for row in rows:
        slug = row["slug"]
        try:
            compile_error = row.get("compile_error")
            if compile_error:
                raise RuntimeError(f"Forge compile failed: {compile_error}")
            code = verify_one(
                slug,
                Path(row["input"]),
                Path(row["output"]),
            )
            status = "pass" if code == 0 else "fail"
            error = None
        except Exception as exc:  # keep later cases observable
            code = 1
            status = "error"
            error = "".join(
                traceback.format_exception_only(type(exc), exc)
            ).strip()
            print(f"{slug} model verification: error: {error}", flush=True)

        failed = failed or code != 0
        results.append(
            {
                "model": slug,
                "status": status,
                "error": error,
            }
        )

    report = {
        "schema": 1,
        "source_sha": manifest.get("source_sha"),
        "status": "fail" if failed else "pass",
        "models": results,
    }
    report_path = manifest_path.parent / "verification-batch.json"
    report_path.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    summary = ", ".join(
        f"{row['model']}={row['status']}" for row in results
    )
    print(f"SolidCraft verification batch: {summary}", flush=True)
    return 1 if failed else 0


def main() -> int:
    """Dispatch batch production, in-runtime execution or case extraction."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "operation",
        nargs="?",
        choices=("batch",),
        default="batch",
    )
    parser.add_argument("--inside-runtime", action="store_true")
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()

    if args.inside_runtime:
        if args.manifest is None:
            parser.error("--inside-runtime requires --manifest")
        return run_inside_runtime(args.manifest)

    if args.manifest is not None:
        parser.error("--manifest requires --inside-runtime")
    return run_host_batch()


if __name__ == "__main__":
    raise SystemExit(main())
