# Forge repository plan

This file is the current source of truth for unfinished work in
`lib.py.solidcraft.forge`.

Forge has two parallel responsibility areas:

1. the **CAD library itself** — public API, compiler/lowering, modelling
   semantics, examples, native qualification and model-specific Verification;
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

Stable integration commit:

`893bfaa6ccb66a10eb033153679c1fe670a6af52`

Accepted durable evidence:

- `main` and `dev-ci` both point to that merge commit;
- `build/main.source_commit` = that exact commit;
- stable Pages source/build-manifest source = that exact commit;
- main integration run `45011944650` — success;
- dev-ci integration run `45011946840` — success.

### Forge release

Current package release: **v0.11.0** at
`9258d54079981604b6dd777a4c4face897c190fe`.

New public work remains under `[Unreleased]`. The next planned package
checkpoint is v0.12.0 after the next coherent post-v0.11 CAD/CI batch.

### SolidCraft runtime

- docker.cad.solidcraft v0.3.4;
- cad-solidcraft:v0.3.4;
- cad-reference:v0.3.4;
- SolidCraft CLI 0.45.0.

### Accepted CAD-CI stack

- `lib.py.cad.ci 0.10.0` @
  `397fb04005b46de8d433cb18c091b1e73714b877`;
- `tool.cad.ci 0.18.0` @
  `b62f9d0b169aa201a3c66c3166f364396b2d71bc`;
- `tool.cad.ci.test` #73 / PR #74;
- complete acceptance run `45010776155` — success;
- Forge explicitly uses `jobs=2`.

The durable long-lived path is now:

```text
one caller runner / one workspace
  -> released tool.cad.ci 0.18.0 durable action
       -> resolve prior scope/base
       -> one CAD-CI/SCons graph
       -> prepare/publish complete build scope
  -> Forge site generation
  -> one Pages publication call
```

No artifact handoff, second runner, second CAD-CI run or Forge-local build-store
orchestration is part of the accepted architecture.

## Recently completed work

- #354: standalone Sketch extrusion Boolean operands, including native
  standalone RoundedRectangle2D.
- #261: model/reference/diagram projection moved to released CAD-CI `copy:`;
  measured post-batch tail reduced from roughly 107-176 s to roughly 49-51 s
  without increasing jobs.
- #662: duplicated Forge durable workflow shell removed in favor of the
  externally accepted tool.cad.ci 0.18.0 same-runner durable action; promoted
  through #663 / #665 to stable `main`.
- #642: Forge v0.11.0 published from exact durable evidence.

## Lane and ownership rule

- `dev-cad` owns Forge CAD API/compiler/model/Verification behavior.
- `dev-ci` owns Forge CI/runtime/publication integration.
- Forge owns shared CAD-CI requirements/design/acceptance governance only where
  explicitly documented; generic implementation still belongs in
  `lib.py.cad.ci`, `tool.cad.ci`, `lib.py.cad.verification` or the runtime
  owner.
- Consumer repositories pin released revisions and must not fork generic
  planners, schedulers, caches, output stores or publishers.

Short-lived feature/fix PRs target one lane and are squash-merged. Exact
`dev-cad -> main` and `dev-ci -> main` promotions use normal merge commits
through the repository `/merge` policy.

## Active workstreams

### WS1 — shared CAD-CI governance and selectivity evidence

Primary lane: `dev-ci` / governance.

#661 is **now**.

Before any new generic capability is requested:

1. refresh the issue's historical 0.17.0/0.9.3 baseline references to the
   accepted 0.18.0/0.10.0 state;
2. inventory which downstream CAD-consumer requirements were already satisfied
   by #261 and #662;
3. measure one-model, no-op and explicit-full scenarios on the current released
   stack;
4. separate actual missing generic selectivity from consumer-local policy;
5. write shared requirements/design/acceptance only for the remaining generic
   gap;
6. implementation, if any, still happens in the correct generic owner repo.

Do not introduce a consumer-local changed-path planner.

### WS2 — connected line/arc Sketch profiles

Primary lane: `dev-cad`.

#567 is **now**, independently of #661.

Pinned SolidCraft 0.45 already exposes the required native primitives:

- `sketch.line`;
- `sketch.arc.center_point`;
- `sketch.arc.three_point`;
- `sketch.arc.tangent`;
- native loose-end/tie diagnostics.

The Forge work is a focused connected-curve profile API that:

1. composes line/arc segments without polygon approximation;
2. keeps expression-valued coordinates and native editability;
3. produces one closed profile accepted by ordinary extrusion;
4. can be consumed by sheet-metal blank creation;
5. does not require caller-authored raw command dictionaries;
6. is proven by saved-design/native command-contract evidence.

#568 follows the connected-profile foundation for native flange/contour work.

### WS3 — terminology governance

#659 is **next/later**.

Now that the durable workflow structure is stable, establish canonical
human-facing build/verification/results terminology and inventory compatibility
names before changing any paths, schemas or public evidence keys.

### WS4 — remaining CAD/reference roadmap

- #568 native sheet-metal flange/contour — **next after #567**.
- #349 focused Revolve child — **later**.
- #570 remove CADCraft from explanatory Verification diagrams — **later**.
- #335 build123d sheet-metal reference semantics — **later**.
- #347 generalized pattern seeds — **later**.
- #9 first-class Sketch/constraints/workplanes — **later** epic.
- #8 hollow primitive intent — **later**.
- #325 AnchorFrame root-cause research — **later**.
- #81 rotated occurrence-local AnchorFrame references — **later**.
- #82 Joints-folder visibility — **later**.
- #175 — **probably obsolete**; consolidate useful evidence into #325.
- #5 — **probably obsolete** in its broad current form; separate any remaining
  constraint scope from #9.

## Open issue assignment — 2026-11-22

| Issue | Lane | Disposition | Next action |
| --- | --- | --- | --- |
| #661 Shared CAD-CI architecture / model-build batch requirements | dev-ci/governance | **now** | Refresh accepted baseline, measure current selectivity, define only remaining generic gap. |
| #567 Mixed line/arc closed Sketch profiles | dev-cad | **now** | Define and implement focused native connected-curve profile API. |
| #568 Native sheet-metal flange/contour | dev-cad | **next** | Continue after #567 establishes reusable connected profiles. |
| #659 Build/verification/results terminology | governance | **next/later** | Establish terminology and compatibility inventory now workflow structure is stable. |
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

## Immediate execution order

1. Run #661 governance/selectivity measurements on the CI lane.
2. In parallel, advance `dev-cad` to the stable baseline and start #567.
3. Start #659 only where it does not rename contracts under active #661/#567
   implementation.
4. Before a second large post-v0.11 batch accumulates, open the planned v0.12.0
   release gate and explicitly include/defer merged work.
