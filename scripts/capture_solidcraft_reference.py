#!/usr/bin/env python3
"""Capture a canonical versioned SolidCraft command-registry snapshot."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
from typing import Any


MIN_COMMAND_COUNT = 100
REQUIRED_COMMANDS = frozenset(
    {
        "engine.commands",
        "solid.box",
        "solid.extrude",
        "sketch.create",
        "sketch.draw.dimensioned",
        "sketch.slot.center_to_center",
    }
)


def validate_registry(value: Any) -> list[dict[str, Any]]:
    """Validate that value looks like the complete SolidCraft command registry."""

    if not isinstance(value, list):
        raise ValueError("SolidCraft command registry must be a JSON array")
    if len(value) < MIN_COMMAND_COUNT:
        raise ValueError(
            f"SolidCraft command registry is implausibly small: "
            f"{len(value)} < {MIN_COMMAND_COUNT}"
        )

    commands: list[dict[str, Any]] = []
    ids: list[str] = []
    for index, row in enumerate(value):
        if not isinstance(row, dict):
            raise ValueError(f"command {index} is not an object")
        command_id = row.get("id")
        label = row.get("label")
        if not isinstance(command_id, str) or not command_id:
            raise ValueError(f"command {index} has no valid id")
        if not isinstance(label, str) or not label:
            raise ValueError(f"command {command_id} has no valid label")
        ids.append(command_id)
        commands.append(row)

    duplicates = sorted({command_id for command_id in ids if ids.count(command_id) > 1})
    if duplicates:
        raise ValueError(f"duplicate SolidCraft command ids: {duplicates}")

    missing = sorted(REQUIRED_COMMANDS - set(ids))
    if missing:
        raise ValueError(f"required SolidCraft commands missing: {missing}")

    return commands


def capture_registry(cli: str) -> tuple[str, list[dict[str, Any]]]:
    """Read exact version and command registry from one SolidCraft CLI binary."""

    version = subprocess.run(
        [cli, "--version"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    registry_text = subprocess.run(
        [cli, "commands"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return version, validate_registry(json.loads(registry_text))


def toolbar(row: dict[str, Any]) -> str:
    tab = str(row.get("tab") or "").strip()
    panel = str(row.get("panel") or "").strip()
    if tab and panel:
        return f"{tab} › {panel}"
    return tab or panel or "–"


def render_commands(commands: list[dict[str, Any]]) -> str:
    """Render the complete registry as a stable human-readable catalog."""

    by_area: dict[str, list[dict[str, Any]]] = {}
    for row in commands:
        area = str(row["id"]).split(".", 1)[0]
        by_area.setdefault(area, []).append(row)

    lines = [
        "# SolidCraft command registry",
        "",
        "Generated from the exact machine-readable output of "
        "`solidcraft-cli commands`.",
        "",
        f"Total registered commands: **{len(commands)}**.",
        "",
    ]
    for area in sorted(by_area):
        lines.extend(
            [
                f"## {area}",
                "",
                "| Command | Id | Toolbar | Planned |",
                "|---|---|---|---|",
            ]
        )
        for row in sorted(by_area[area], key=lambda item: str(item["id"])):
            planned = str(row.get("planned") or "")
            lines.append(
                "| "
                + str(row["label"]).replace("|", "\\|")
                + " | `"
                + str(row["id"])
                + "` | "
                + toolbar(row).replace("|", "\\|")
                + " | "
                + planned.replace("|", "\\|")
                + " |"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def source_text(
    *,
    version: str,
    cli_version: str,
    upstream_commit: str,
    runtime_release: str,
    runtime_image: str,
    count: int,
) -> str:
    return f"""# SolidCraft {version} canonical reference snapshot

This directory is generated from the command registry emitted by the qualified
immutable SolidCraft runtime. It is not a hand-authored Forge migration note.

- SolidCraft release: `v{version}`
- Upstream commit: `{upstream_commit}`
- Qualified runtime release: `{runtime_release}`
- Qualified runtime image: `{runtime_image}`
- Captured CLI version: `{cli_version}`
- Registered commands: `{count}`

## Canonical evidence

- `commands.json` is the exact normalized JSON registry captured from
  `solidcraft-cli commands`.
- `commands.md` is generated from `commands.json` for human review.

Forge compatibility conclusions must be traceable to this captured registry,
the exact runtime behavior, or separately recorded upstream source evidence.
Do not replace this directory with a manually selected command subset.
"""


def write_snapshot(
    *,
    out: Path,
    version: str,
    cli_version: str,
    upstream_commit: str,
    runtime_release: str,
    runtime_image: str,
    commands: list[dict[str, Any]],
) -> None:
    out.mkdir(parents=True, exist_ok=True)
    normalized = sorted(commands, key=lambda row: str(row["id"]))
    (out / "commands.json").write_text(
        json.dumps(normalized, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (out / "commands.md").write_text(
        render_commands(normalized),
        encoding="utf-8",
    )
    (out / "SOURCE.md").write_text(
        source_text(
            version=version,
            cli_version=cli_version,
            upstream_commit=upstream_commit,
            runtime_release=runtime_release,
            runtime_image=runtime_image,
            count=len(normalized),
        ),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cli", default="solidcraft-cli")
    parser.add_argument("--version", required=True)
    parser.add_argument("--upstream-commit", required=True)
    parser.add_argument("--runtime-release", required=True)
    parser.add_argument("--runtime-image", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    cli_version, commands = capture_registry(args.cli)
    expected = f"0.{args.version.split('.', 1)[1]}" if args.version.startswith("0.") else args.version
    if args.version not in cli_version:
        raise SystemExit(
            f"CLI version mismatch: expected {args.version!r} in {cli_version!r}"
        )
    write_snapshot(
        out=args.out,
        version=args.version,
        cli_version=cli_version,
        upstream_commit=args.upstream_commit,
        runtime_release=args.runtime_release,
        runtime_image=args.runtime_image,
        commands=commands,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
