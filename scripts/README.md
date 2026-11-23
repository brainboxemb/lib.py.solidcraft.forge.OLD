# Forge repository scripts

This directory contains **Forge-owned repository helpers** used by package
testing, model/reference verification, site evidence, governance and release
publication.

These scripts are not the generic CAD-CI engine. Generic selection, planning,
SCons execution, caching, durable build storage, Pages publication and the
installed `cad-ci` executable belong to `lib.py.cad.ci`. Released GitHub
workflow/governance integration belongs to `tool.cad.ci`.

This README documents the current scripts and their callers. It does not imply
that every script is a stable public API.

## Package and example mechanics

| Script | Responsibility | Current caller / consumer |
| --- | --- | --- |
| `forge_example.py` | Shared mechanics for locating the exact built Forge wheel, running example contract tests, compiling Forge models and writing command documents. It deliberately does not decide CI scope. | Imported by Forge package/model/reference verification scripts. |
| `tool_ci.py` | Build/test adapter for the Forge Python package and its repository test suite. | `forge-tests` CAD-CI item; package-related tests. |
| `tool_verify.py` | Release-level verification of the built Forge wheel against a fixed representative example set and expected rejection set. | `forge-release` CAD-CI item. |
| `model_contract_test.py` | Run one model's Forge command-contract tests against the exact built wheel. | Model item template in root `cad-ci.yml`. |

## Native model verification

| Script | Responsibility | Current caller / consumer |
| --- | --- | --- |
| `model_verification_batch.py` | Run active declarative Forge model verification as one shared SolidCraft-runtime batch and write per-model results. Process-driving portions remain under #713 review and must move behind owner APIs when generic. | `model-verification-batch` CAD-CI item. |
| `qualification_summary.py` | Compose already-produced verification evidence into Forge's public qualification semantics; it does not execute CAD. | Forge test/site evidence paths; semantic composition comes from released verification library. |

The model batch is the only model-verification process entry point. It imports
`verification/model_verification.py`, which owns Forge native-model production,
and `verification/model_visual.py`, which owns Forge-specific camera/snapshot
adaptation. Those are ordinary modules, not scripts or secondary launchers.

## Independent reference verification

| Script | Responsibility | Current caller / consumer |
| --- | --- | --- |
| `reference_verification_batch.py` | Run all active independent reference implementations in one shared reference runtime and write per-reference evidence. Forge catalog selection/projection may remain; generic runtime/verification process mechanics remain an #713 migration target. | `reference-verification-batch` CAD-CI item. |
| `build_diagrams.py` | Render the versioned Forge verification-diagram sources. | Shared reference batch; diagram sources live under `verification/diagrams/sources/`. |

## Verification dependency packaging

| Script | Responsibility | Current caller / consumer |
| --- | --- | --- |
| `verification_package.py` | Temporary compatibility transport for the exact released `lib.py.cad.verification` wheel. Remove it when Forge adopts released CAD-CI `verification_package` injection; do not preserve it as a permanent package layer. | `cad-verification-package` CAD-CI item; configuration in `ci/cad-verification-package/package.json`. |

## SolidCraft runtime reference

| Script | Responsibility | Current caller / consumer |
| --- | --- | --- |
| `capture_solidcraft_reference.py` | Capture and validate a canonical versioned SolidCraft command-registry snapshot. | Maintainer/reference-update workflow; snapshots under `docs/reference/solidcraft/`. |
| `verify_solidcraft_reference_runtime.py` | Compare a checked command-registry snapshot with the exact immutable SolidCraft runtime. | `solidcraft-reference` CAD-CI item. |

## Repository governance

Forge owns no merge-policy implementation script. The repository's thin
`.github/workflows/merge-policy.yml` wrapper consumes the exact released
tool.cad.ci reusable merge-policy workflow. Merge-method decisions, current-head
checks, branch lifecycle and allow-listed post-merge cleanup therefore remain in
the shared tool owner rather than in this scripts directory.

## Release publication

The release helpers live in `scripts/release/` because they form one contract.

| Script | Responsibility | Current caller / consumer |
| --- | --- | --- |
| `release/validate_release.py` | Validate one exact Forge release candidate against source, changelog and durable build/Page evidence. | `.github/workflows/release.yml`, release-policy tests, and publisher. |
| `release/publish_release.py` | Publish an already-validated Forge release/tag from exact durable evidence. | `.github/workflows/release.yml`. |
| `release/test_validate_release.py` | Regression tests for release-candidate validation. | `release-policy` CAD-CI item. |
| `release/test_publish_release.py` | Regression tests for publication behavior. | `release-policy` CAD-CI item. |

The authoritative release contract is [`docs/release.md`](../docs/release.md).

## Removed legacy launchers

- `model_verify.py` — superseded by the declarative shared batch. No active
  caller remains; current CI tests explicitly require it not to be wired.
- `verification_evidence.py` — superseded by the shared reference batch. No
  active caller remains.

## Ownership rule

When editing a script, first identify which category above owns the behavior:

- Forge API/compiler/model behavior stays in Forge;
- generic CAD-CI behavior and the installed CLI belong in `lib.py.cad.ci`;
- GitHub workflow/governance adapters belong in `tool.cad.ci`;
- generic model/reference verification belongs in `lib.py.cad.verification`;
- immutable runtime/dependency packaging belongs in its runtime owner repository.

Do not add a Forge-local workaround for behavior owned by one of those generic
repositories. New or retained top-level scripts must have an active caller and
a Forge-owned process-entry reason; otherwise use a package module or remove
the launcher.

## Related documentation

- [Repository-level CI items](../ci/README.md)
- [Root CAD-CI configuration](../cad-ci.yml)
- [Repository plan](../docs/plan.md)
- [Repository requirements](../docs/requirements.md)
- [Repository design](../docs/design.md)
- [Examples](../examples/README.md)
