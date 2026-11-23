# Forge repository plan

This file is the current source of truth for unfinished work in
`lib.py.solidcraft.forge`.

Forge owns the public CAD API/compiler/model behavior, Forge-specific
verification expectations and repository-specific model/build adapters.
Generic CAD-CI, shared release flow, reusable verification, runtime packaging,
generated build branches, Pages and merge policy stay in their owner
repositories.

## Current repository state

Permanent source refs:

```text
main
dev-cad
dev-ci
```

Current heads:

- `main`: `68905bdbd4d999d73248858b4c3f9336ad47cf6e`;
- `dev-ci`: `68905bdbd4d999d73248858b4c3f9336ad47cf6e`;
- `dev-cad`: `84cb5b4b6b7085eb92865eafe28fd7478bb2665e`.

The two development branches now have separate jobs:

- `dev-ci`: finish the central release-flow adoption;
- `dev-cad`: continue Forge CAD/API fixes.

Do not mix those two kinds of change in one branch.

### Forge package release

Current published Forge package: **v0.12.0** at
`68905bdbd4d999d73248858b4c3f9336ad47cf6e`.

#739 is promoted to stable `main` and #714 published v0.12.0 through the
central CAD release flow. Release run `45250563106` succeeded; the annotated
`v0.12.0` tag resolves to the exact source above and the GitHub Release is
published.

### Shared CI/release stack

- `lib.py.cad.ci v0.18.2` @
  `088644a05ff698957aef2ddc6cc5de037ddfa158`;
- `tool.cad.ci v0.36.1` @
  `8a9acb8ea69581728a3850c658b4c1ae2db6ff5a` is released;
- v0.36.1 central CAD release-flow external acceptance is complete in
  `tool.cad.ci.test #256`;
- `tool.py.lib.ci v0.2.1` @
  `58ead6897a4ac8cafef22a3c1f834491bf61568d` owns the generic
  tag/GitHub Release transaction;
- `lib.py.cad.verification v0.16.0` @
  `c7c145b7be0c602724e8cca874ef29990baaad1e`;
- `docker.cad.solidcraft v0.3.4` remains the pinned runtime image.

## Permanent branch rule

- `main`: stable integration only.
- `dev-cad`: Forge API/compiler/model/verification/site-content work.
- `dev-ci`: CI/release integration.
- short-lived branches are squash-merged;
- exact `dev-cad|dev-ci -> main`: normal history-preserving merge;
- exact `main -> dev-cad|dev-ci`: normal history-preserving merge;
- generic owner behavior is changed, released and externally tested in its
  owner repository before Forge consumes it.

## Active work

### dev-ci — central release flow

Status: **complete on stable main**.

1. **complete** — remove the Forge-local CAD build/Page release check (#763,
   PR #769);
2. **complete upstream** — `tool.cad.ci v0.36.1` provides the central CAD
   release workflow;
3. **complete upstream** — black-box v0.36.1 acceptance in
   `tool.cad.ci.test #256`;
4. **complete** — #739 / PR #772 adopted the exact released central release
   wrapper;
5. **complete** — PR #774 promoted exact `dev-ci -> main` through the shared
   history-preserving merge policy at
   `68905bdbd4d999d73248858b4c3f9336ad47cf6e`;
6. **complete** — exact main durable run `45250190637` succeeded;
7. **complete** — #714 published and verified Forge v0.12.0 through the central
   flow.

Pages remains web output and is not release evidence.

### dev-cad — Forge API/compiler work

Status: **active in parallel**.

Completed on `dev-cad`:

1. #746 Cone boolean join/cut support — PR #766, merge
   `611762e4f2eb1be02ec758f4a86cb519f1419fbc`;
2. #747 Polygon2D in explicit/attached Sketch — PR #768, merge
   `4625e57b39b344cb64ed4063cb7ea7c933fa7b15`, including a real
   SolidCraft runtime regression;
3. #748 STL export — closed as not Forge-owned; the CAD consumer uses the
   supported SolidCraft CLI directly from the accepted saved `.sc` model.

Current order:

1. **complete on dev-cad** — #749 model-local import isolation, PR #770,
   merge `fd836e4797a7672497fc63978902ff2306fd9b7a`;
2. **complete on dev-cad** — #750 rotated local Sketch frame for standalone
   prism/cutter Shapes, PR #771, merge
   `84cb5b4b6b7085eb92865eafe28fd7478bb2665e`;
3. **now — metal** — #773 native `sheet.hem` on existing sheet bodies;
4. **next metal candidate** — #776 native `sheet.path_flange`, reusing the
   existing-sheet history and #683 open-chain contract;
5. #753 component-local native Cylinder joins across copied/rotated
   occurrences;
6. #751 native SolidCraft exploded views — deliberately lower priority.

#335 build123d Sheet Metal reference is currently upstream-blocked: the latest
released build123d v0.13.0 is otherwise identical to v0.12.0 and neither
released tag contains the newer Sheet Metal API shown by current development
documentation. Do not replace the reference with another solid approximation or
pin an unreleased upstream revision.

Each issue uses its own branch from current `dev-cad` and returns to
`dev-cad` only after focused tests are green.

## Open issue assessment — 2026-11-23

| Issue | Owner/branch | Status | Next action |
| --- | --- | --- | --- |
| #739 Adopt central CAD release flow | dev-ci/main | **complete** | PR #772 plus permanent-lane PR #774 put the released wrapper on stable main. |
| #714 Release Forge 0.12.0 | main/release | **complete** | v0.12.0 is published and verified at exact `68905bdbd4d999d73248858b4c3f9336ad47cf6e`. |
| #746 Cone boolean feature compilation | dev-cad | **implemented on dev-cad** | Keep open until the CAD batch reaches stable main/release. |
| #747 Polygon2D explicit/attached Sketch | dev-cad | **implemented on dev-cad** | Keep open until the CAD batch reaches stable main/release. |
| #749 Isolate project-local modules between run_script roots | dev-cad | **implemented on dev-cad** | PR #770 is green and merged; keep open until the CAD batch reaches stable main/release. |
| #750 Standalone Shape local transform/rotation | dev-cad | **implemented on dev-cad** | PR #771 is merged; keep open until the CAD batch reaches stable main/release. |
| #773 Native sheet.hem | dev-cad | **now / metal** | Add the focused public API, native lowering, tests and SolidCraft regression without a solid approximation. |
| #776 Native sheet.path_flange | dev-cad | **after #773 / metal** | Reuse the existing sheet-history and open-chain contracts; keep it separate from #773. |
| #753 Component-local Cylinder joins across copied/rotated occurrences | dev-cad | **after metal slice** | Refresh the existing focused draft against current dev-cad and qualify it. |
| #751 Native SolidCraft exploded views | dev-cad | **later / lower priority** | Resume after the higher-priority metal/runtime work. |
| #713 Audit/reduce Forge scripts | repository | **later** | Remove only genuine duplicates after the release-flow migration. |
| #737 Historical changelog alignment | docs | **later / docs-only** | Keep separate from functional work. |
| #659 Standardize build/verification/results terminology | cross-repo | **later** | Follow the shared plain-language work; do not mix into #749. |
| #570 Remove CADCraft from verification diagrams | dev-cad | **later** | Replace source format while preserving presentation behavior. |
| #349 Remaining SOLID CREATE coverage | dev-cad | **later** | Deliver focused features only when required. |
| #347 Generalized pattern seeds | dev-cad | **later** | Generalize by native feature identity. |
| #335 build123d Sheet Metal reference | dev-cad/upstream | **blocked on released build123d Sheet Metal API** | Keep the current limitation explicit; use the first suitable released upstream version, never an unreleased pin or another solid approximation. |
| #325 AnchorFrame root cause | dev-cad | **later** | Resume when an active model requires it. |
| #175 HUB75-like AnchorFrame diagnostic | dev-cad | **probably obsolete** | Move any unique evidence into #325. |
| #82 Joints-folder visibility | dev-cad | **later** | Decide interaction/export policy later. |
| #81 Rotated occurrence-local AnchorFrame references | dev-cad | **later** | Investigate with #325. |
| #9 First-class Sketch/constraints/workplanes | dev-cad | **later** | Keep as the broad epic; implement focused slices separately. |
| #8 Hollow primitives | dev-cad | **later** | Reconcile with native shell/pipe/boolean support when needed. |
| #5 Generic anchors/parametric constraints | dev-cad | **probably obsolete** | Separate any remaining useful scope from #9. |

## Boundary

Forge may own:

- compiler/API behavior;
- `run_script()` model loading;
- Forge-specific builder commands;
- model-specific SolidCraft verification definitions;
- visual/presentation policy;
- site content/rendering.

Forge must not own:

- generic CAD-CI planning/SCons/cache behavior;
- generic build-record validation;
- generic release command/tag/GitHub Release handling;
- Pages publication mechanics;
- reusable CAD verification internals;
- generic merge policy.

## Next checkpoint

Continue #773 on `dev-cad`; after its exact-head and durable lane evidence are
green, continue with #776 as the next metal slice. Forge v0.12.0 and the central
release-flow migration are complete. Exploded-view #751 stays lower priority.
