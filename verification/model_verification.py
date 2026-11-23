"""Forge-owned native-model producer used inside the shared verification batch.

The process boundary lives in `scripts/model_verification_batch.py`. This module
only replays compiled Forge commands into the initial native SolidCraft model,
loads model-owned verification data and delegates generic checks/evidence to the
released `lib.py.cad.verification` API.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import runpy
import time

ROOT = Path(__file__).resolve().parents[1]


def verify_path(slug: str) -> Path:
    """Return one model-local declarative verification file."""

    return ROOT / "examples" / slug / "verification" / "verify.py"


def load_definition(path: Path):
    """Load one data-only model definition inside the released runtime."""

    namespace = runpy.run_path(str(path))
    definition = namespace.get("VERIFICATION")

    from cad_verification import SolidCraftVerification

    if not isinstance(definition, SolidCraftVerification):
        raise RuntimeError(
            f"verification file must export SolidCraftVerification: {path}"
        )
    return definition


def produce_native_model(input_path: Path, output_dir: Path) -> Path:
    """Replay Forge output into the initial editable SolidCraft model."""

    from scpf.headless import run_document

    value = json.loads(input_path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(
            f"Forge command document must contain one object: {input_path}"
        )

    native = output_dir / "native"
    native.mkdir(parents=True, exist_ok=True)
    model = native / "model.sc"

    run_document(
        value,
        save=model,
        export=native / "model.step",
        results_out=native / "results.json",
        replay_log_out=native / "replay-log.json",
        work_dir=native / "replay_work",
    )
    return model


def run_inside_runtime(
    slug: str,
    input_path: Path,
    output_dir: Path,
) -> int:
    """Produce the native model and hand all verification to the library."""

    inside_started = time.perf_counter()

    entry_ms = os.environ.get("FORGE_CONTAINER_ENTRY_MS", "").strip()
    if entry_ms:
        python_bootstrap_s = (
            time.time_ns() // 1_000_000 - int(entry_ms)
        ) / 1000.0
        print(
            f"FORGE TIMING python_bootstrap_s={python_bootstrap_s:.3f}",
            flush=True,
        )

    import_started = time.perf_counter()
    from cad_verification import run_solidcraft_verification
    print(
        "FORGE TIMING "
        f"cad_verification_import_s={time.perf_counter() - import_started:.3f}",
        flush=True,
    )

    path = verify_path(slug)
    if not path.is_file():
        raise RuntimeError(f"missing verification file: {path}")

    definition_started = time.perf_counter()
    definition = load_definition(path)
    print(
        "FORGE TIMING "
        f"definition_load_s={time.perf_counter() - definition_started:.3f}",
        flush=True,
    )

    native_started = time.perf_counter()
    model = produce_native_model(input_path.resolve(), output_dir.resolve())
    print(
        "FORGE TIMING "
        f"native_model_s={time.perf_counter() - native_started:.3f}",
        flush=True,
    )

    verification_started = time.perf_counter()
    report = run_solidcraft_verification(
        model,
        output_dir.resolve(),
        definition,
    )
    print(
        "FORGE TIMING "
        f"solidcraft_verification_s={time.perf_counter() - verification_started:.3f}",
        flush=True,
    )

    measurements = output_dir.resolve() / "baseline" / "measurements.json"
    visual_report = None
    visual_policy = path.parent / "visual.json"
    if visual_policy.is_file():
        from verification.model_visual import run_visual_verification

        visual_started = time.perf_counter()
        visual_report = run_visual_verification(
            model,
            measurements,
            visual_policy,
            output_dir.resolve(),
        )
        print(
            "FORGE TIMING "
            f"visual_verification_s={time.perf_counter() - visual_started:.3f}",
            flush=True,
        )

    from verification.model_visual import write_presentation_preview

    preview_started = time.perf_counter()
    write_presentation_preview(
        model,
        measurements,
        output_dir.resolve(),
    )
    print(
        "FORGE TIMING "
        f"presentation_preview_s={time.perf_counter() - preview_started:.3f}",
        flush=True,
    )

    print(
        "FORGE TIMING "
        f"inside_runtime_total_s={time.perf_counter() - inside_started:.3f}",
        flush=True,
    )
    print(f"{slug} model verification: {report['status']}", flush=True)
    if report["status"] != "pass":
        failed = next(
            (
                row for row in report.get("checks", ())
                if row.get("status") in {"fail", "error"}
            ),
            None,
        )
        if failed is not None:
            print(
                f"{slug} verification failure: "
                + json.dumps(
                    {
                        "id": failed.get("id"),
                        "status": failed.get("status"),
                        "error": failed.get("error"),
                        "evidence": failed.get("evidence"),
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
    if visual_report is not None:
        print(
            f"{slug} visual verification: {visual_report['status']}",
            flush=True,
        )

    passed = report["status"] == "pass"
    if visual_report is not None:
        passed = passed and visual_report["status"] == "pass"
    return 0 if passed else 1
