# Repository-level CAD-CI items

This directory contains **Forge-owned repository CI items and builders**.

Generic discovery, SCons execution, built-in CAD builders, reusable mesh
verification, durable build storage and Pages publication belong to the exact
released `lib.py.cad.ci` / `tool.cad.ci` stack.

The root [`cad-ci.yml`](../cad-ci.yml) discovers repository items together
with `scpf/ci.yml` and the model/reference items below `examples/`.
Executable Forge-specific behavior lives under `ci/builders/<name>/builder.yml`;
normal item `ci.yml` files select a builder and remain declarative.

## Current item map

| Item | Purpose | Depends on | Forge-owned implementation |
| --- | --- | --- | --- |
| `forge-tests` | Run the Forge Python unit/integration suite against the exact built Forge package. | `forge-package` | `ci/builders/forge-tests`, `scripts/tool_ci.py`. |
| `forge-release` | Release-level verification of the exact built Forge package. | `forge-package` | `ci/builders/forge-release`, `scripts/tool_verify.py`. |
| `model-verification-batch` | Produce native SolidCraft verification for active Forge model consumers in one shared runtime batch. | `forge-package` plus builder capability `verification_package: true` | `ci/builders/model-verification-batch`, model verification scripts. |
| `reference-verification-batch` | Produce only the remaining Forge-owned PythonSCAD/pyBOSL2 reference evidence plus diagram working output. | builder capability `verification_package: true` | `ci/builders/reference-verification-batch`, `scripts/reference_verification_batch.py`, presentation helpers. |
| `release-policy` | Validate Forge release-candidate/publication policy without CAD runtimes. | none | `ci/builders/release-policy`, `scripts/release/*`. |
| `site-source` | Validate Forge site source, metadata and evidence adapters without CAD runtimes. | none | `ci/builders/site-source`, `site/test_*.py`. |
| `solidcraft-reference` | Verify the checked SolidCraft command-registry snapshot against the pinned immutable runtime. | none | `ci/builders/solidcraft-reference`, `scripts/verify_solidcraft_reference_runtime.py`. |
| `verification-diagrams` | Project diagrams already produced by the remaining Forge reference batch. | `reference-verification-batch` | `ci/builders/verification-diagrams`. |

The Forge package itself is the `forge-package` item in
[`scpf/ci.yml`](../scpf/ci.yml).

## Generic reference path

CadQuery and build123d are **not** repository-level Forge batch work anymore.

Each `examples/<slug>/cadquery` or `build123d` item selects the released
built-in builder and the first-class `mesh-geometry` verification adapter.
The released library owns verification-package materialization and its internal
graph nodes. Forge consumes only public contracts:

```text
root verification.package pin
  -> built-in CadQuery/build123d verification
  -> Forge repository builders declaring verification_package: true
       -> CAD_CI_VERIFICATION_WHEEL
```

Forge configuration and scripts must not name the synthesized internal package
item.

One compatible reference container is shared by active built-in items;
build123d rows share one runtime-owned isolated interpreter process. Forge owns
only each model's `model.py` and
`verification/reference_geometry.json`.

PythonSCAD/pyBOSL2 remain in `reference-verification-batch` until a released
generic owner contract exists for those engines.

## Pages

Pages is not a normal CI item. Root `cad-ci.yml` declares:

```yaml
publication:
  pages:
    builder: pages-site
    output: site
```

`ci/builders/pages-site` renders Forge content from the complete durable scope
and exact source/build provenance supplied by CAD-CI. The released tool/library
own stable/named Pages placement and publication.

## Ownership

Forge builders may implement repository-specific package commands, SolidCraft
verification, PythonSCAD/pyBOSL2 reference execution, diagrams and site
rendering. They must not implement generic selection, scheduling, caching,
verification-package transport, built-in build123d/CadQuery batching, durable
state or Pages publication.

Related documentation:

- [Repository plan](../docs/plan.md)
- [Repository requirements](../docs/requirements.md)
- [Repository design](../docs/design.md)
- [Release contract](../docs/release.md)
- [Examples](../examples/README.md)
- [Scripts](../scripts/README.md)
