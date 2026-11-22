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

- `lib.py.cad.ci 0.11.0` @
  `e621daf6e309bdd0e3f643a12007f1b66490696d`;
- `tool.cad.ci 0.19.0` @
  `5677c41a61929b32ab2cb07087a6505f7b9347d8`;
- `tool.cad.ci.test` #80 / PR #81 / acceptance run
  `45022699789` — success, including the released shared merge-policy contract.

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

### WS1 — shared CI/governance lane

Primary lane: `dev-ci`. **Independent of this CAD lane.**

- #674 shared merge/lane policy adoption — **now**.
- released `tool.cad.ci 0.19.0` is adopted by Forge;
- PR #695 proved the thin consumer wrapper and green `dev-ci` integration;
- #696 / PR #697 proved the live short-lived path: squash merge, allow-listed
  temporary-head cleanup and dispatched `dev-ci` integration;
- the remaining #674 proof is exact long-lived `dev-ci -> main` promotion:
  normal merge commit, lane preservation and successful dispatched integration.
- CAD-library work below does not wait on that independent promotion proof.

### WS2 — native sheet-metal work

#568 is now a tracking parent for the actual SolidCraft 0.45 flange family.
The previous wording assumed a separate `sheet.contour` command and incorrectly
treated #567's closed-profile builder as the contour foundation.

Current 0.45 split:

- #682 native `sheet.flange(type=edge)` — **complete**; merged and natively qualified;
- #683 reusable open connected Sketch curve chains — **complete**;
  PR #694 merged to `dev-cad` as `9b3b47aa97b49bcc3a08919572e6ddfd2ad28831`
  after PR run `45025059775` proved the complete 39-model SolidCraft batch,
  and policy-dispatched `dev-cad` integration run `45025329364` succeeded.
- #684 native `sheet.flange(type=contour)` — **effectively complete but still open**; draft PR #698 is implemented as one focused native slice and PR run `45027053821` is green across unit/compiler contracts, save/reopen mutation, flat-pattern inspection and the complete SolidCraft model batch. Merge through `/merge`, then close only after the policy-dispatched `dev-cad` integration succeeds.
  Native qualification shows that a tangent-arc contour flat pattern is recoverable but reports zero discrete `bends`; flat-pattern rule/thickness/K-factor and `bend_count=0` are qualified, while bend radius remains proven by the emitted sheet rule.

#### #682 focused contract

Public API:

```python
sheet.flange(
    edges=[(40, -20, 2)],
    height=20,
    angle=90,
    height_from=None,
    position=None,
    flip=False,
)
```

Initial scope:

- explicit fixed XYZ edge-pick points only;
- positive parameter-capable flange `height`;
- parameter-capable `angle`, default 90°;
- optional exact SolidCraft 0.45 `height_from`: `outer|inner|tangent`;
- optional exact SolidCraft 0.45 `position`: `inside|outside|middle|material_outside|tangent`;
- `flip` boolean;
- existing sheet rule owns thickness, K-factor and bend radius.

Out of scope for #682: per-edge dictionaries/segments, radius override, corner
relief override, chained `then` bends, new generic edge-selector architecture.

Qualification must prove native edge-flange history, flat-pattern continuity and
saved-design height/angle mutation.
- #568 parent — **tracking**, complete only when the required child slices are accepted;
- #349 focused Revolve child first — **later**.

Do not combine #682/#683/#684 back into one large sheet-metal PR. Edge flange
and open-chain contour are different public API/compiler contracts.

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
| #674 Shared merge/lane policy adoption | dev-ci | **now** | Short-lived policy path is proven; perform exact `dev-ci -> main` promotion through `/merge` and verify normal merge + lane preservation. |
| #568 SolidCraft 0.45 sheet flange coverage parent | dev-cad | **now** | Track the active #684 contour-flange child; #682 and #683 are complete. |
| #684 Native contour flange | dev-cad | **effectively complete but still open** | PR #698 run `45027053821` is green; merge through `/merge`, then require successful dispatched `dev-cad` integration before closure. |
| #679 Namespace repeated component-local feature names | dev-cad | **next** | Resume after #684 unless downstream HUB75 work makes it an immediate blocker. |
| #659 Standardize build/verification/results terminology | cross-repo | **later** | Coordinate after current #674 governance proof so architecture and vocabulary do not move together. |
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
| #5 Generic anchors/parametric constraints | dev-cad | **probably obsolete** | Separate any remaining constraint scope from overlap with #9. |

## Recently completed

- #683 reusable open connected Sketch chains — PR #694 merged to `dev-cad`; native batch `45025059775` and lane integration `45025329364` are green.
- #682 native sheet edge flange — merged to `dev-cad` in PR #687 with native
  SolidCraft 0.45 history, saved-design height/angle mutation and flat-pattern
  qualification.
- #661/#688 selective shared model batch — promoted through `dev-ci -> main`
  after one-model, no-op and full-run qualification.

- #567 mixed line/arc closed Sketch profiles — merged to `dev-cad`; shared native line/arc lowering, ordinary extrusion and sheet-metal consumption are covered by unit contracts and `connected-profile-sheet` baseline/saved-design SolidCraft verification.
## Next release checkpoint

Before a second large post-v0.11 batch accumulates, open the planned v0.12.0
release issue and explicitly include/defer the merged CAD/CI work. Do not bump
source metadata before that release gate exists.
