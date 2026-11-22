# Forge repository plan

This file is the current source of truth for unfinished work in
`lib.py.solidcraft.forge`.

Forge has two independent responsibility areas:

1. the CAD library itself — public API, compiler/lowering, modelling semantics,
   examples, native qualification and model-specific Verification;
2. CI/runtime/Verification integration around that library — exact released
   generic CAD-CI consumption, immutable runtime consumption, durable build/Page
   publication and release mechanics.

`dev-cad` and `dev-ci` advance independently unless they share a real owner
release or architecture gate.

## Current accepted baseline

Permanent source lanes:

```text
main
dev-cad
dev-ci
```

Current stable integration commit:

`893bfaa6ccb66a10eb033153679c1fe670a6af52`

Accepted post-v0.11 integration now includes:

- #354 standalone Sketch Boolean operands;
- #261 dependency-output `copy:` integration and jobs=2 runtime reduction;
- #662 durable workflow cut-over to one released same-runner action;
- durable `build/main` and stable Pages provenance on exact
  `893bfaa6...`.

### Forge release

Current package release: **v0.11.0** at
`9258d54079981604b6dd777a4c4face897c190fe`.

New user-visible work remains under `[Unreleased]`. The next planned package
checkpoint remains v0.12.0 after a coherent post-v0.11 CAD/CI batch reaches
main.

### SolidCraft runtime

- docker.cad.solidcraft v0.3.4;
- cad-solidcraft:v0.3.4;
- cad-reference:v0.3.4;
- SolidCraft CLI 0.45.0.

### Accepted generic CAD-CI stack

Current externally accepted stack:

- `lib.py.cad.ci 0.10.0` @
  `397fb04005b46de8d433cb18c091b1e73714b877`;
- `tool.cad.ci 0.18.0` @
  `b62f9d0b169aa201a3c66c3166f364396b2d71bc`;
- `tool.cad.ci.test` #73 / PR #74 / acceptance run
  `45010776155` — success.

The released root composite action is the accepted long-lived durable path:

```text
one runner / one workspace
  -> checkout/bootstrap exact tool + pinned library once
  -> resolve prior durable scope/base
  -> one CAD-CI/SCons graph
  -> prepare/publish complete durable build scope
  -> Forge site generation
  -> Pages publication
```

Forge does not duplicate generic build-scope discovery, build-store update or
build publication in workflow YAML. There is no artifact handoff or second
durable runner.

Forge remains explicitly on `jobs=2`.

## Lane rule

- `dev-cad`: Forge API/compiler/model/Verification/site-content behavior.
- `dev-ci`: CAD-CI/runtime/publication integration.
- Generic CI behavior is fixed and released in lib.py.cad.ci/tool.cad.ci first.
- Generic Verification behavior is fixed and released in lib.py.cad.verification first.
- Runtime packaging is fixed and released in docker.cad.solidcraft first.

Short-lived branches target one lane and are squash-merged. Exact
`dev-cad -> main` and `dev-ci -> main` promotions use the repository
`/merge` policy and therefore normal merge commits.

## Active workstreams

### WS1 — #661 shared CAD-CI batch/selectivity governance

Primary lane: `dev-ci`. **Now.**

The shared batch/copy pattern is working and the durable workflow structure is
now stable. The remaining ecosystem question is whether a one-model change can
restrict the shared model-build batch itself, rather than merely selecting the
top-level CAD-CI graph correctly.

Required evidence on the current released stack:

1. one-model edit;
2. no-op run;
3. explicit complete run.

For each, capture:

- selected top-level SCons items;
- models actually executed by the shared batch;
- reused/current results;
- runtime image pulls/container starts;
- total batch duration and provenance.

If Forge already meets the required selectivity contract, close #661 with
evidence and let downstream CAD consumers adopt the same pattern.

If a generic gap is demonstrated, define the missing requirement here and open
the technical implementation issue in the actual owner
(`lib.py.cad.ci`, `tool.cad.ci` or verification) before any consumer change.

Do not add a Forge- or consumer-local changed-path planner.

### WS2 — #567 mixed line/arc closed Sketch profiles

Primary lane: `dev-cad`. **Now, parallel with #661.**

Pinned SolidCraft 0.45 native commands already provide the required low-level
building blocks:

- `sketch.line`;
- `sketch.arc.center_point`;
- `sketch.arc.three_point`;
- `sketch.arc.tangent`;
- stable created curve/point ids;
- `sketch.loose_ends` / tie diagnostics.

Next action is a focused Forge connected-curve profile API that:

- preserves authored line/arc intent;
- produces a genuinely closed native profile;
- works for ordinary extrusion;
- provides the foundation needed by the sheet-metal contour/flange work;
- does not fall back to Polygon2D approximation or raw caller command
  dictionaries.

Requirements/design/API contract must be written before implementation.

#### #567 branch status

Requirements, design and public API text are written on `issue/567-connected-curve-profile`.
The builder records `connected_profile` intent and validates authoring/closure, but the current branch does not yet lower that profile kind in either standalone or attached Sketch compilation.

Next implementation order:

1. add one shared connected-profile lowering helper for native `sketch.line`, `sketch.arc.three_point` and `sketch.arc.center_point` with `connect=true`;
2. use it from standalone Sketch compilation so ordinary extrusion and `sheet_metal()` share exactly one lowering path;
3. use the same helper from attached Sketch lowering where the existing profile contract permits it;
4. add focused unit/command-contract coverage before adding the native qualification example;
5. add the small native saved-design qualification case required by #567, then measure it on the immutable SolidCraft 0.45 runtime.

No polygon approximation, raw caller command dictionaries or second sheet-metal-only profile compiler.

### WS3 — next CAD-library work

- #568 native sheet-metal flange/contour — **next** after #567 profile
  foundation.
- #349 focused Revolve child first — **later**.

### WS4 — cross-repository terminology and Verification/reference quality

- #659 build/verify/results terminology — **later**; coordinate after #661 so
  architecture and vocabulary do not change at the same time.
- #570 remove CADCraft from Verification diagrams — **later**.
- #335 build123d sheet-metal reference semantics — **later**.

### WS5 — API coverage and interaction research

- #347 generalized pattern seeds — **later**.
- #9 first-class Sketch/constraints/workplanes — **later** epic.
- #8 hollow primitive intent — **later**.
- #325 AnchorFrame root-cause research — **later**.
- #81 rotated occurrence-local AnchorFrame references — **later**.
- #82 Joints-folder visibility — **later**.
- #175 — **probably obsolete**; consolidate useful evidence into #325.
- #5 — **probably obsolete** in current broad form; separate any remaining
  constraint scope from #9.

## Open issue assignment — 2026-11-22

| Issue | Lane | Status | Next action |
| --- | --- | --- | --- |
| #661 Govern shared CAD-CI architecture and consumer model-build batch requirements | dev-ci | **now** | Measure one-model/no-op/full batch selectivity on tool 0.18.0/lib 0.10.0 before deciding whether a generic owner change is required. |
| #567 Mixed line/arc closed Sketch profiles | dev-cad | **now** | Define connected line/arc profile API and native lowering contract, then implement focused qualification. |
| #568 Native sheet-metal flange/contour | dev-cad | **next** | Qualify immutable runtime contracts after #567 connected-profile foundation. |
| #659 Standardize build/verification/results terminology | cross-repo | **later** | Start after #661 architecture decision. |
| #349 Remaining SOLID › CREATE coverage | dev-cad | **later** | Split focused Revolve child for latch work. |
| #570 Remove CADCraft from Verification diagrams | dev-cad | **later** | Replace explanatory sources without moving generic rendering into Forge. |
| #335 build123d Sheet Metal reference | dev-cad | **later** | Replace solid approximation with actual sheet-metal workflow. |
| #347 Patterns accept any applied Shape feature | dev-cad | **later** | Generalize seed validation by native feature identity. |
| #325 AnchorFrame regression root cause | dev-cad | **later** | Resume only when it becomes an active dependency. |
| #81 Inline rotated AnchorFrame references | dev-cad | **later** | Investigate occurrence-local frames with #325. |
| #82 Joints folder visibility | dev-cad | **later** | Decide interaction/export policy later. |
| #9 First-class Sketch/constraints/workplanes | dev-cad | **later** | Refresh epic and deliver focused slices. |
| #8 Tube/RectTube/OvalTube | dev-cad | **later** | Reconcile intent with native shell/pipe/boolean histories. |
| #175 HUB75-like AnchorFrame diagnostic | dev-cad | **probably obsolete** | Consolidate useful evidence into #325, then close/rewrite. |
| #5 Generic anchors/parametric constraints | dev-cad | **probably obsolete** | Separate remaining constraint scope from overlap with #9. |

## Next release checkpoint

Before a second large post-v0.11 batch accumulates, open the planned v0.12.0
release issue and explicitly include/defer the merged CAD/CI work. Do not bump
source metadata before that release gate exists.
