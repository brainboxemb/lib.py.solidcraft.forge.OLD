# Forge repository plan

This file is the current source of truth for unfinished work in
`lib.py.solidcraft.forge`.

Forge has two parallel responsibility areas:

1. the **CAD library itself** — public API, compiler/lowering, modelling
   semantics, examples, qualification and model-specific verification;
2. the **CI/runtime/verification integration around that library** — released
   generic CAD-CI consumption, immutable runtime consumption, durable
   build/Page publication and Forge release mechanics.

Neither area is subordinate to the other. `dev-cad` and `dev-ci` progress
independently unless a real owner release or architecture gate connects them.

## Current accepted baseline

Permanent source lanes:

```text
main
dev-cad
dev-ci
```

Stable integration:

- `main`:
  `7238a6d515106835b56a2bf6b208dd67da2d061e`;
- `dev-ci`:
  `7238a6d515106835b56a2bf6b208dd67da2d061e`;
- durable `build/main` source commit:
  `7238a6d515106835b56a2bf6b208dd67da2d061e`;
- stable Pages source/build-manifest source:
  `7238a6d515106835b56a2bf6b208dd67da2d061e`.

The #261 dependency-output-copy integration is therefore fully promoted.

### Forge package release

Current package release: **v0.11.0** at
`9258d54079981604b6dd777a4c4face897c190fe`.

New public work remains under `[Unreleased]`. The next planned package
checkpoint remains v0.12.0 after a coherent post-v0.11 CAD/CI batch reaches
`main`.

### SolidCraft runtime

- docker.cad.solidcraft v0.3.4;
- cad-solidcraft:v0.3.4;
- cad-reference:v0.3.4;
- SolidCraft CLI 0.45.0.

### CAD-CI stack

Current Forge `main` consumes:

- `tool.cad.ci 0.17.1` @
  `1012e6a539a2fddd8194124844fe208bf16cf4e4`;
- `lib.py.cad.ci 0.10.0` @
  `397fb04005b46de8d433cb18c091b1e73714b877`;
- jobs=2.

That stack delivered #261 and reduced the measured post-batch SCons tail from
roughly 107-176 s to roughly 49-51 s without increasing jobs.

A newer exact tool release is externally accepted but **not yet consumed by
Forge**:

- `tool.cad.ci 0.18.0` @
  `b62f9d0b169aa201a3c66c3166f364396b2d71bc`;
- same `lib.py.cad.ci 0.10.0` pin;
- `tool.cad.ci.test` #73 / PR #74;
- acceptance run `45010776155` — success;
- durable same-runner action, reusable workflows and complete existing suite
  all passed.

#662 owns adoption of that exact release.

## Recently completed work

- #354: standalone Sketch extrusion Boolean operands, including standalone
  RoundedRectangle2D, promoted through `dev-cad -> main`.
- #261: shared model/reference/diagram projection migrated to released CAD-CI
  `copy:`; jobs remained 2; promoted through `dev-ci -> main`.
- #642: Forge v0.11.0 published from exact durable evidence.
- #649: handoff/AGENTS corrected to describe both CAD-library and CI/integration
  responsibilities.

## Lane and ownership rule

- `dev-cad` owns Forge CAD API/compiler/model/verification behavior.
- `dev-ci` owns Forge CI/runtime/publication integration.
- Forge may own ecosystem-level requirements/acceptance for shared CAD-CI
  behavior, but implementation still belongs in the actual generic owner
  repository (`lib.py.cad.ci`, `tool.cad.ci`,
  `lib.py.cad.verification`, or runtime owner). #661 owns the explicit
  governance contract and must reconcile this wording in permanent docs.
- Consumer repositories pin released revisions and must not fork generic
  planners, schedulers, caches, output stores or publishers.

Short-lived feature/fix PRs target one development lane and are squash-merged.
Exact `dev-cad -> main` and `dev-ci -> main` promotions use normal merge
commits through the repository `/merge` policy.

## Active workstreams

### WS0 — #662 durable workflow simplification

Primary lane: `dev-ci`. **Now.**

The current Forge push/manual workflow still duplicates generic durable
scope/base/build-publication shell that now belongs to released
`tool.cad.ci 0.18.0`.

Required result:

```text
one runner / one workspace
  -> exact tool.cad.ci 0.18.0 durable action
       -> resolve durable scope/base
       -> one CAD-CI/SCons run, jobs=2
       -> prepare/publish complete build scope
  -> Forge-owned site/build.py
  -> one generic cad_ci_tool publish pages call
```

Constraints:

- no second runner;
- no artifact handoff;
- no second CAD-CI graph;
- no repeated tool/library bootstrap;
- preserve main/dev-cad/dev-ci durable scope semantics;
- preserve stable-main Pages subtree preservation for dev-cad/dev-ci;
- preserve PR docs-only skip and promotion-full-run policy without adding a
  classifier job.

Workflow tests must reject the old local durable scope/fetch/update/publish
blocks once migration is complete.

### WS1 — shared CAD-CI governance

#661 is **next** on the CI/governance lane.

It establishes Forge as requirements/design/acceptance governance for shared
CAD-CI behavior while keeping implementation in the generic owner repository.
Before implementation, refresh its historical baseline references from
0.17.0/0.9.3 to the actually accepted 0.18.0/0.10.0 state and audit which
consumer-model batch requirements are already satisfied by #261/#662.

#659 is **next/later** governance work: standardize human-facing
build/verify/results terminology across Forge and CAD repositories without
blindly renaming compatibility paths or schemas.

### WS2 — next CAD-library work

Primary lane: `dev-cad`.

#567 is **next**:

- expose a focused connected line/arc closed-profile API;
- use qualified SolidCraft 0.45 native sketch line/arc commands;
- preserve editability and expression support;
- prove ordinary extrusion and sheet-metal blank use without polygon
  approximation or caller-authored raw command dictionaries.

Then:

- #568 native sheet-metal flange/contour;
- #349 focused Revolve child first, broader SOLID › CREATE inventory later.

### WS3 — verification/reference quality

- #570 remove CADCraft from explanatory verification diagrams — later.
- #335 build123d sheet-metal reference semantics — later.

### WS4 — API coverage roadmap

- #347 generalized pattern seeds — later.
- #9 first-class Sketch/constraints/workplanes — later epic.
- #8 hollow primitive intent — later.

### WS5 — AnchorFrame / interaction research

- #325 root-cause research — later.
- #81 rotated occurrence-local AnchorFrame references — later.
- #82 Joints-folder visibility — later.
- #175 probably obsolete; consolidate retained evidence into #325.
- #5 probably obsolete in current broad form; separate remaining constraints
  from already delivered anchor behavior and overlap with #9.

## Open issue assignment — 2026-11-22

| Issue | Lane | Disposition | Next action |
| --- | --- | --- | --- |
| #662 Consume tool.cad.ci 0.18.0 durable action | dev-ci | **now** | Replace duplicated durable shell with one same-runner released action; keep Forge site + Pages on that runner. |
| #661 Shared CAD-CI governance/model-build batch requirements | governance/dev-ci | **next** | Refresh baseline, reconcile already-delivered #261/#662 behavior, then define remaining shared acceptance contract. |
| #659 Build/verification/results terminology | governance | **next/later** | Establish terminology in permanent docs; inventory compatibility names before any migration. |
| #567 Mixed line/arc closed Sketch profiles | dev-cad | **next** | Deliver focused connected-curve profile API on native line/arc contracts. |
| #568 Native sheet-metal flange/contour | dev-cad | **next** | Qualify immutable runtime contracts before API exposure. |
| #349 Remaining SOLID › CREATE coverage | dev-cad | **next** | Split focused Revolve child for latch work. |
| #570 Remove CADCraft from verification diagrams | dev-cad | **later** | Replace explanatory sources without moving generic rendering into Forge. |
| #335 build123d Sheet Metal reference | dev-cad | **later** | Replace solid approximation with actual sheet-metal workflow. |
| #347 Patterns accept any applied Shape feature | dev-cad | **later** | Generalize seed validation by native feature identity. |
| #325 AnchorFrame regression root cause | dev-cad | **later** | Resume when it becomes an active dependency. |
| #81 Inline rotated AnchorFrame references | dev-cad | **later** | Investigate occurrence-local frames with #325. |
| #82 Joints folder visibility | dev-cad | **later** | Decide interaction/export policy later. |
| #9 First-class Sketch/constraints/workplanes | dev-cad | **later** | Refresh epic and deliver focused slices. |
| #8 Tube/RectTube/OvalTube | dev-cad | **later** | Reconcile intent with native shell/pipe/boolean histories. |
| #175 HUB75-like AnchorFrame diagnostic | dev-cad | **probably obsolete** | Consolidate useful evidence into #325, then close/rewrite. |
| #5 Generic anchors/parametric constraints | dev-cad | **probably obsolete** | Separate remaining constraint scope from overlap with #9. |

## Immediate execution order

1. #662 workflow simplification on `dev-ci`.
2. After #662 is accepted/promoted, sync `dev-cad` to the stable baseline and
   start #567.
3. #661 and #659 may progress in parallel as governance work where they do not
   change the #662 execution contract.
4. Before a second large post-v0.11 batch accumulates, open the planned v0.12.0
   release gate and explicitly include/defer merged work.
