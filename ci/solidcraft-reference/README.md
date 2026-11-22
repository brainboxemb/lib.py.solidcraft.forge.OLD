# solidcraft-reference

Repository-level verification item for Forge's checked SolidCraft command
reference.

## Purpose

Forge keeps version-pinned SolidCraft command-registry reference data under
`docs/reference/solidcraft/<version>/`. This item verifies the checked snapshot
against the exact immutable SolidCraft runtime consumed by Forge.

## Contract

- **Item id:** `solidcraft-reference`
- **Kind:** `verification`
- **Dependencies:** none
- **Verifier:**
  [`scripts/verify_solidcraft_reference_runtime.py`](../../scripts/verify_solidcraft_reference_runtime.py)
- **Snapshot helper:**
  [`scripts/capture_solidcraft_reference.py`](../../scripts/capture_solidcraft_reference.py)
- **Current checked runtime:** `cad-solidcraft:v0.3.4`, SolidCraft `0.45.0`
- **Current snapshot:** `docs/reference/solidcraft/0.45.0/commands.json`

The runtime image itself is owned and released by
`docker.cad.solidcraft`; this item only verifies Forge's pinned consumer
reference.

See the repository-level [CI map](../README.md).
