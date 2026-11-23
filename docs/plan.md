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

- `main`: `74e44e98bb561992547609b24b2e2664356423a1`;
- `dev-ci`: `8d8bf2ad7e229500a75f8c1e3043cb8245de01d6`;
- `dev-cad`: `4625e57b39b344cb64ed4063cb7ea7c933fa7b15`.

The two development branches now have separate jobs:

- `dev-ci`: finish the central release-flow adoption;
- `dev-cad`: continue Forge CAD/API fixes.

Do not mix those two kinds of change in one branch.

### Forge package release

Current published Forge package: **v0.11.0** at
`9258d54079981604b6dd777a4c4face897c190fe`.

The v0.12.0 source preparation is already on `main`. Publication is blocked
only by the release-flow migration in #739.

The failed old release run created no `v0.12.0` tag or GitHub Release.

### Shared CI/release stack

- `lib.py.cad.ci v0.18.2` @
  `088644a05ff698957aef2ddc6cc5de037ddfa158`;
- `tool.cad.ci v0.36.0` @
  `093eafb0eabf6b6617ec82dde17a76fdc718ae12` is released;
- v0.36.0 central CAD release-flow external acceptance is running in
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

Status: **blocked only on external acceptance**.

1. **complete** — remove the Forge-local CAD build/Page release check (#763,
   PR #769);
2. **complete upstream** — `tool.cad.ci v0.36.0` now provides the central
   CAD release workflow and checks the stable main `ci-build-record`;
3. **now outside Forge** — finish black-box v0.36.0 acceptance in
   `tool.cad.ci.test #256`;
4. after #256 passes, #739 replaces Forge's local generic release workflow
   with the exact released `tool.cad.ci v0.36.0` consumer template;
5. require `dev-ci` green, then merge exact `dev-ci -> main`;
6. require the resulting main build green;
7. publish Forge v0.12.0 through the central CAD release flow and verify the
   exact tag/GitHub Release.

Pages is web output and is not release evidence.

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
2. **now** — #750 rotated local Sketch frame for standalone prism/cutter Shapes;
3. #751 native SolidCraft exploded views;
4. #753 component-local native Cylinder joins across copied/rotated
   occurrences.

Each issue uses its own branch from current `dev-cad` and returns to
`dev-cad` only after focused tests are green.

## Open issue assessment — 2026-11-23

| Issue | Owner/branch | Status | Next action |
| --- | --- | --- | --- |
| #739 Adopt central CAD release flow | dev-ci | **blocked on tool.cad.ci.test #256** | After external v0.36.0 acceptance, copy the released CAD release template and remove Forge-local generic release code. |
| #714 Release Forge 0.12.0 | main/release | **blocked on #739** | Publish only after #739 reaches main and the exact main build is green. |
| #746 Cone boolean feature compilation | dev-cad | **implemented on dev-cad** | Keep open until the CAD batch reaches stable main/release. |
| #747 Polygon2D explicit/attached Sketch | dev-cad | **implemented on dev-cad** | Keep open until the CAD batch reaches stable main/release. |
| #749 Isolate project-local modules between run_script roots | dev-cad | **implemented on dev-cad** | PR #770 is green and merged; keep open until the CAD batch reaches stable main/release. |
| #750 Standalone Shape local transform/rotation | dev-cad | **now** | Add a rotated explicit Sketch frame so standalone extruded cutters can be translated/rotated before normal CSG. |
| #751 Native SolidCraft exploded views | dev-cad | **next** | Wrap and qualify native explode behavior after #750. |
| #753 Component-local Cylinder joins across copied/rotated occurrences | dev-cad | **after #751** | Refresh the existing focused draft against current dev-cad and qualify it. |
| #713 Audit/reduce Forge scripts | repository | **later** | Remove only genuine duplicates after the release-flow migration. |
| #737 Historical changelog alignment | docs | **later / docs-only** | Keep separate from functional work. |
| #659 Standardize build/verification/results terminology | cross-repo | **later** | Follow the shared plain-language work; do not mix into #749. |
| #570 Remove CADCraft from verification diagrams | dev-cad | **later** | Replace source format while preserving presentation behavior. |
| #349 Remaining SOLID CREATE coverage | dev-cad | **later** | Deliver focused features only when required. |
| #347 Generalized pattern seeds | dev-cad | **later** | Generalize by native feature identity. |
| #335 build123d Sheet Metal reference | dev-cad | **later** | Replace the current reference approximation. |
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

Continue #750 on `dev-cad` while `tool.cad.ci.test #256` runs independently.
When #256 passes, finish #739 on `dev-ci` and release Forge v0.12.0 through
the central CAD release flow.
