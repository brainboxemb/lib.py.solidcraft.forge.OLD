"""Diagnostic A/B for Forge #845 contour-flange recess replay.

Runs the exact minimal fixture in three forms against one SolidCraft CLI:
1. normal Forge phased replay (save/reopen between binding phases);
2. one fully resolved native script in a single SolidCraft process;
3. the same resolved script with only sketch.create plane.fixed=true.

The single-process cases intentionally do not change geometry or cut depth.
"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import urllib.request
import zipfile

from scpf.headless import run_document
from scpf.runner import run_script


ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "examples/sheet-contour-flange-recess/scpf/model.py"


def download_and_extract(url: str, root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    archive = root / Path(url).name
    if not archive.exists():
        print(f"Downloading {url}", flush=True)
        urllib.request.urlretrieve(url, archive)

    extract = root / "solidcraft"
    if extract.exists():
        shutil.rmtree(extract)
    extract.mkdir()

    if archive.suffix == ".zip":
        with zipfile.ZipFile(archive) as zf:
            zf.extractall(extract)
    elif archive.name.endswith(".tar.gz"):
        with tarfile.open(archive, "r:gz") as tf:
            tf.extractall(extract)
    else:
        raise RuntimeError(f"unsupported SolidCraft archive: {archive.name}")

    names = {"solidcraft-cli", "solidcraft-cli.exe"}
    matches = [p for p in extract.rglob("*") if p.is_file() and p.name in names]
    if len(matches) != 1:
        raise RuntimeError(f"expected one solidcraft-cli executable, found: {matches}")
    cli = matches[0]
    if sys.platform != "win32":
        cli.chmod(cli.stat().st_mode | 0o111)
    return cli


def resolved_document(log: dict) -> dict:
    commands = log.get("commands")
    if not isinstance(commands, list) or not commands:
        raise RuntimeError("replay log has no commands")
    return {
        "commands": [
            {
                "command": row["command"],
                "params": row["resolved_params"],
            }
            for row in commands
        ]
    }


def fixed_variant(document: dict) -> dict:
    fixed = copy.deepcopy(document)
    found = 0
    for row in fixed["commands"]:
        if row["command"] != "sketch.create":
            continue
        params = row.get("params", {})
        if params.get("name") != "Broad face recess":
            continue
        plane = params.get("plane")
        if not isinstance(plane, dict) or "face" not in plane:
            raise RuntimeError("Broad face recess is not an attached face Sketch")
        plane["fixed"] = True
        found += 1
    if found != 1:
        raise RuntimeError(f"expected one Broad face recess sketch.create, found {found}")
    return fixed


def run_native(cli: Path, document: dict, output: Path, label: str) -> dict:
    script = output / f"{label}.json"
    results = output / f"{label}-results.json"
    save = output / f"{label}.sc"
    script.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    command = [
        str(cli),
        "run",
        str(script),
        "--param-check",
        "strict",
        "--results",
        "--json-out",
        str(results),
        "--save",
        str(save),
    ]
    completed = subprocess.run(command, text=True, capture_output=True)
    outcome = {
        "label": label,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "saved": save.exists(),
    }
    print(f"\n=== {label}: returncode={completed.returncode} ===")
    if completed.stdout.strip():
        print(completed.stdout)
    if completed.stderr.strip():
        print(completed.stderr, file=sys.stderr)
    return outcome


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--asset-url", required=True)
    parser.add_argument("--output", type=Path, default=Path("diagnostic-845"))
    args = parser.parse_args(argv)

    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    cli = download_and_extract(args.asset_url, output / "runtime")
    print(f"SolidCraft CLI: {cli}")
    subprocess.run([str(cli), "--version"], check=True)

    document = run_script(MODEL)
    replay = output / "replay.json"
    replay.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")

    phased_log = output / "phased-replay-log.json"
    run_document(
        document,
        save=output / "phased.sc",
        results_out=output / "phased-results.json",
        replay_log_out=phased_log,
        executable=str(cli),
        work_dir=output / "phases",
    )
    print("=== phased replay: PASS ===")

    log = json.loads(phased_log.read_text(encoding="utf-8"))
    normal = resolved_document(log)
    fixed = fixed_variant(normal)

    normal_outcome = run_native(cli, normal, output, "single-normal")
    fixed_outcome = run_native(cli, fixed, output, "single-fixed")

    summary = {
        "phased": "pass",
        "single_normal": normal_outcome,
        "single_fixed": fixed_outcome,
    }
    (output / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )

    print("\n=== summary ===")
    print(json.dumps({
        "phased": "pass",
        "single_normal_returncode": normal_outcome["returncode"],
        "single_fixed_returncode": fixed_outcome["returncode"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
