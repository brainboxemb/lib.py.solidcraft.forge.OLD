# Forge repository plan

This file is the current source of truth for unfinished work in
`lib.py.solidcraft.forge`.

Forge is first and foremost the central CAD library: public API, compiler/lowering,
modelling semantics, reusable CAD capabilities, examples and Forge-owned verification
expectations. CI/runtime/Verification integration is supporting infrastructure around
that library and must remain delegated to its generic owner repositories where the
behavior is not Forge-specific.

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

- `lib.py.cad.ci 0.11.0` @
  `e621daf6e309bdd0e3f643a12007f1b66490696d`;
- `tool.cad.ci 0.18.1` @
  `e29d3127d5d3f9310f3cab4e27430a64a61c21cc`;
- `tool.cad.ci.test` #77 / PR #78 / acceptance run
  `45019713862` — success.

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

#### CI item audit — 2026-11-22

All nine current `ci/*` items are present in durable `build/main` and `build/dev-ci`
and still have a distinct current responsibility. None is currently classified
as obsolete.

| CI item | Status | Note |
| --- | --- | --- |
| `cad-verification-package` | **current** | Prepares the exact released verification-library dependency once for model/reference consumers. |
| `forge-tests` | **current** | Tests the exact built Forge package; separate from release verification. |
| `forge-release` | **current** | Exact-candidate release evidence consumed by the release validator. |
| `model-verification-batch` | **current; improvement active** | Shared SolidCraft runtime remains desired; #661 addresses coarse internal selected-model granularity. |
| `reference-verification-batch` | **current** | Shared heavy reference runtime for independent CAD implementations and diagram production. |
| `release-policy` | **current** | Tests release validator/publisher without CAD runtimes and is an explicit release gate. |
| `site-source` | **current** | Keeps presentation/source validation independent from CAD execution. |
| `solidcraft-reference` | **current; low-frequency guard** | Verifies the checked SolidCraft command registry against the immutable runtime. |
| `verification-diagrams` | **current; implementation transition planned** | Public/site diagram evidence is still consumed; #570 removes CADCraft while preserving the diagram responsibility. |

Do not remove or combine an item merely to reduce directory count. Any future
structural simplification needs a separate requirements/design decision after
the current responsibilities and consumers remain preserved.

### WS1 — #661 / #688 selective shared model batch qualification

Primary lane: `dev-ci`. **Now; implementation merged, qualification active.**

#681 merged the accepted `selection_context: direct_dependents` consumer
implementation to `dev-ci` at `601fcd7fef7b17610fbdef32e8c5352bf7ba6788`.

Remaining proof is tracked by #688:

1. one-model `simple-box` source probe on the merged implementation;
2. remove that probe before merge;
3. durable `dev-ci` no-model run after the plan/evidence merge;
4. explicit complete run through the normal `dev-ci -> main` promotion path.

For each run record top-level targets, `active_dependents`, models actually
executed, container starts and duration. The temporary model probe must never
land on `dev-ci`.

Measurement 1 is complete:

- PR #690 / run `45021440751` selected six top-level targets;
- shared batch received only `simple-box`;
- one SolidCraft container processed only `simple-box=pass`;
- batch timing: pull 8.481 s, container/process 3.705 s, total 12.336 s;
- pre-fix comparison: run `45014107995` processed all 36 models with ~63.198 s container/process.

The temporary `simple-box` probe is removed before merge.

Close #661 only after the remaining no-model durable run and explicit full
promotion run are recorded. Reference-batch sparse selection remains outside
this work.
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
| #661 Validate shared batch/selectivity as a Forge consumer | dev-ci | **blocked on #688 proof** | Implementation merged in #681; close after one-model/no-op/full qualification is recorded. |
| #688 Qualify selective Forge model batch | dev-ci | **now** | Run temporary one-model probe, remove it before merge, then record no-op durable and promotion full-run evidence. |
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
