# Forge scripts

This directory contains Forge-owned integration entry points. It is **not** a
second CAD-CI or verification framework.

Generic CAD-CI planning, execution, builders, durable scopes and publication
belong to `lib.py.cad.ci`. Released GitHub workflow/governance integration
belongs to `tool.cad.ci`. Generic verification mechanics belong to
`lib.py.cad.verification`. Runtime/container composition belongs to
`docker.cad.solidcraft`.

Every retained script below must have a concrete Forge-owned responsibility and
an active caller.

| Script | Caller | Classification | Status |
| --- | --- | --- | --- |
| `build_diagrams.py` | `reference_verification_batch.py`; `ci/reference-verification-batch` | Forge verification-diagram producer using the selected reference runtime | keep pending #570 |
| `capture_solidcraft_reference.py` | `verify_solidcraft_reference_runtime.py`; maintenance capture | Forge checked command-registry normalization/validation | keep |
| `forge_example.py` | model/package verification scripts | shared Forge package/example helper module; not a standalone CI entry point | keep |
| `model_contract_test.py` | `cad-ci.yml` model template | thin Forge adapter for model-owned command-contract tests | keep |
| `model_verification_batch.py` | `ci/model-verification-batch/ci.yml` | Forge active-model batch producer; process-driving portions remain under #713 review | reduce |
| `model_verify_declarative.py` | model verification batch/tests | Forge native-model producer plus verification-library adapter; generic verification mechanics must stay in the released library | reduce |
| `model_visual.py` | declarative model verification/tests | Forge SolidCraft camera/snapshot adapter; generic image/regression mechanics stay in verification library | keep/review |
| `qualification_summary.py` | `site/build.py`; tests | Forge public five-check presentation mapping over already-produced evidence | keep |
| `reference_verification_batch.py` | `ci/reference-verification-batch/ci.yml` | Forge reference-catalog batch producer; generic runtime/verification mechanics remain owner-layer responsibilities | reduce |
| `tool_ci.py` | Forge package/test CI items | Forge package build/test adapter | keep |
| `tool_verify.py` | `ci/forge-release/ci.yml` | Forge release-qualification adapter for representative examples | keep |
| `verification_package.py` | `ci/cad-verification-package/ci.yml` | compatibility transport for the exact verification wheel | **temporary; remove when Forge adopts released CAD-CI verification-package injection** |
| `verify_solidcraft_reference_runtime.py` | `ci/solidcraft-reference/ci.yml` | Forge check of the versioned command snapshot against the selected immutable runtime | keep |
| `release/validate_release.py` | release workflow/publisher/tests | Forge-specific release gate | keep |
| `release/publish_release.py` | `.github/workflows/release.yml` | Forge-specific release publication | keep |
| `release/test_validate_release.py` | `ci/release-policy/ci.yml` | release-policy test entry point | keep |
| `release/test_publish_release.py` | `ci/release-policy/ci.yml` | release-publication test entry point | keep |

## Removed legacy launchers

- `model_verify.py` — superseded by the declarative shared batch; no active
  caller remains and current CI tests explicitly require it not to be wired.
- `verification_evidence.py` — superseded by the shared reference batch; no
  active caller remains.

## Rules for new work

1. Do not add a script merely to bridge two Python APIs that can call each other
   directly.
2. Do not put generic CAD-CI selection, scheduling, caching or publication
   behavior here.
3. Do not put generic verification algorithms or result semantics here.
4. Prefer a package module for reusable Forge code and a single thin script
   only when CAD-CI, GitHub Actions or the release process needs a process
   entry point.
5. Update this file in the same change whenever a retained script is added,
   removed or changes owner/caller.
