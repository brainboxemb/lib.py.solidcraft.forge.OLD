# Repository-level CAD-CI items

This directory contains **repository-level CI items for Forge**.

These are not Forge CAD models and they are not a second generic CI framework.
Generic discovery, planning, SCons execution, build-store handling and Pages
publication belong to the released `lib.py.cad.ci` / `tool.cad.ci` stack.

The root [`cad-ci.yml`](../cad-ci.yml) discovers these items together with
`scpf/ci.yml` and the model/reference items below `examples/`.

This README documents the **current layout only**. It is not a decision that
this directory structure is ideal or permanent. Structural changes require a
separate issue/design decision.

## Item map

| Item | Purpose | Depends on | Primary implementation / consumer |
| --- | --- | --- | --- |
| `cad-verification-package` | Build the exact released `lib.py.cad.verification` wheel used by Forge verification. | none | `scripts/verification_package.py`; consumed by the model/reference verification batches. |
| `forge-tests` | Run the Forge Python unit/integration test suite against the exact built Forge package. | `forge-package` | `scripts/tool_ci.py`; also covers merge-policy and qualification-summary tests. |
| `forge-release` | Release-level verification of the exact built Forge package with a fixed representative example set. | `forge-package` | `scripts/tool_verify.py` and `scripts/forge_example.py`. |
| `model-verification-batch` | Produce native SolidCraft verification evidence for the active Forge model catalog in one shared runtime batch. | `forge-package`, `cad-verification-package` | `scripts/model_verification_batch.py`, `scripts/model_verify_declarative.py`, `scripts/model_visual.py`. Individual model items copy their result from this batch. |
| `reference-verification-batch` | Produce independent build123d/CadQuery/pyBOSL2/PythonSCAD reference evidence in one shared reference-runtime batch. | `cad-verification-package` | `scripts/reference_verification_batch.py`, reference helpers under `verification/`, and `scripts/build_diagrams.py`. Reference child items copy their result from this batch. |
| `release-policy` | Validate Forge release-candidate and publication policy without starting CAD runtimes. | none | `scripts/release/validate_release.py`, `scripts/release/publish_release.py` and their tests; contract in `docs/release.md`. |
| `site-source` | Validate Forge site source, example metadata and build-evidence expectations without starting CAD runtimes. | none | `site/test_build_evidence.py`, `site/test_example_metadata.py`, `site/test_site.py`. |
| `solidcraft-reference` | Verify the checked SolidCraft command-registry snapshot against the pinned immutable runtime. | none | `scripts/verify_solidcraft_reference_runtime.py`; snapshot source under `docs/reference/solidcraft/`. |
| `verification-diagrams` | Publish/copy verification diagrams already produced by the shared reference batch. | `reference-verification-batch` | Engine-owned dependency copy; diagram sources under `verification/diagrams/sources/`. |

## How these items fit together

The Forge package itself is built by [`scpf/ci.yml`](../scpf/ci.yml) as
`forge-package`.

The important dependency paths are:

```text
forge-package
  ├─ forge-tests
  ├─ forge-release
  └─ model-verification-batch
       └─ examples/<model> model verification result

cad-verification-package
  ├─ model-verification-batch
  └─ reference-verification-batch
       ├─ examples/<model>/<reference implementation>
       └─ verification-diagrams
```

The root `cad-ci.yml` owns repository-wide templates, runtime variables and
item discovery. Item files in this directory contain only Forge-repository
configuration and commands; they must not implement generic selection,
scheduling, caching or publication behavior.

## Related documentation

- [Repository plan](../docs/plan.md) — current unfinished work and ordering.
- [Repository requirements](../docs/requirements.md) — Forge product/consumer requirements.
- [Repository design](../docs/design.md) — Forge architecture and owner boundaries.
- [Release contract](../docs/release.md) — Forge package release validation/publication.
- [Examples](../examples/README.md) — model/reference item structure.
- [Scripts](../scripts/README.md) — implementation helper inventory.
