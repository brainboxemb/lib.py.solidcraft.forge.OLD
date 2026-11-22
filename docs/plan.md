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

`7238a6d515106835b56a2bf6b208dd67da2d061e`

That baseline includes:

- #354 standalone Sketch Boolean operands;
- #261 dependency-output `copy:` integration and jobs=2 runtime improvement;
- durable `build/main` and stable Pages provenance on the same exact source
  commit.

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
- `tool.cad.ci.test` #73 / PR #74;
- acceptance run `45010776155` — success.

The released 0.18.0 root composite action provides the accepted same-runner
long-lived durable path:

```text
checkout/bootstrap once
  -> resolve prior durable scope/base
  -> one CAD-CI/SCons graph
  -> prepare/publish complete durable build scope
  -> return prepared scope/build commit to later steps on the same runner
```

No artifact handoff or second post-action runner is part of that contract.

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

### WS1 — #662 simplify Forge workflow around released durable action

Primary lane: `dev-ci`. **Now.**

The current push/manual Forge workflow still duplicates generic durable
orchestration in local YAML:

- durable build-scope lookup/base resolution;
- generic CAD-CI action invocation with manually resolved selection;
- build-branch fetch;
- complete scope update/prepare;
- durable build publication.

That duplication is now obsolete because tool.cad.ci 0.18.0 owns the same
sequence in one externally accepted same-runner composite action.

Required cut-over:

1. pin exact tool.cad.ci 0.18.0;
2. keep the PR path one job and preserve its current docs-only/full-promotion
   policy without adding a classifier runner;
3. replace the push/manual local durable shell blocks with one released
   `tool.cad.ci@b62f9d0b...` durable action step;
4. keep Forge-owned site generation immediately after that action on the same
   runner using `prepared_scope` and `build_commit` outputs;
5. keep one generic Pages publication call after site generation;
6. preserve main/dev-cad/dev-ci scope semantics and stable-main preservation of
   named Pages subtrees;
7. keep jobs=2;
8. update tests to reject reintroduction of local durable scope/build
   orchestration;
9. prove named and main durable build/Page provenance before promotion.

Performance constraint: **do not** split the durable path into separate
reusable-workflow jobs, runners or artifacts.

### WS2 — #661 shared CAD-CI batch/selectivity governance

Primary lane: `dev-ci`. **Next.**

The shared batch/copy pattern is already working. Measure one-model, no-op and
explicit-full scenarios on the current released stack before deciding whether a
new generic selectivity capability is required for downstream CAD consumers.

Do not implement consumer-local changed-path planners.

### WS3 — CAD-library next work

Primary lane: `dev-cad`.

1. #567 mixed line/arc closed Sketch profiles — **next**;
2. #568 native sheet-metal flange/contour — **next** after #567 contract;
3. #349 focused Revolve child first — **later**.

### WS4 — cross-repository terminology and Verification/reference quality

- #659 build/verify/results terminology — **later**; coordinate after #662 so
  workflow names/outputs are not renamed during the durable cut-over.
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
| #662 Consume tool.cad.ci 0.18.0 durable action and simplify Forge workflow | dev-ci | **now** | Replace duplicated durable push orchestration with one released same-runner action and prove build/Page provenance. |
| #661 Govern shared CAD-CI architecture and consumer model-build batch requirements | dev-ci | **next** | Measure one-model/no-op/full batch selectivity on the current released stack. |
| #567 Mixed line/arc closed Sketch profiles | dev-cad | **next** | Design focused connected line/arc profile API from pinned SolidCraft 0.45 native commands. |
| #568 Native sheet-metal flange/contour | dev-cad | **next** | Qualify immutable runtime contracts after the connected-profile foundation. |
| #659 Standardize build/verification/results terminology | cross-repo | **later** | Start after #662 so workflow structure and terminology do not change simultaneously. |
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
