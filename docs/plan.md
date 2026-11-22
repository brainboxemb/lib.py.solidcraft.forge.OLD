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

### WS1 — shared CI/governance lane

Primary lane: `dev-ci`. **Independent of this CAD lane.**

- #661/#688 selective shared model batch qualification is complete and promoted
  to `main`; the accepted 0.18.1/0.11.0 stack is proven for one-model, no-op
  and explicit full-run cases.
- #674 shared merge/lane policy extraction is the next generic governance item;
  normative implementation is owned by `tool.cad.ci#103`, not by Forge-local
  CI code.
- CAD-library work below does not wait on #674.

### WS2 — native sheet-metal work

#568 is now a tracking parent for the actual SolidCraft 0.45 flange family.
The previous wording assumed a separate `sheet.contour` command and incorrectly
treated #567's closed-profile builder as the contour foundation.

Current 0.45 split:

- #682 native `sheet.flange(type=edge)` — **complete**; merged and natively qualified;
- #683 reusable open connected Sketch curve chains — **now**; generic Sketch capability;
  Native qualification found that SolidCraft 0.45 `sketch.arc.tangent.end` accepts only a concrete `[x,y]`; update the documented initial contract and reject parameterized tangent endpoints before replay while keeping line endpoints parametric.
  The follow-up native run proved replay itself succeeds, but Forge's producer unconditionally requested STEP export and SolidCraft rejected the intentional zero-body design (`nothing to export`). This is Forge-owned producer behavior, not a verification-library gap: classify the narrow parameter/sketch-only replay, save the editable `.sc` and results without `--out`, and omit body-dependent presentation preview for that case.
- #684 native `sheet.flange(type=contour)` — **blocked on #683**;

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
| #674 Shared merge/lane policy extraction | dev-ci / tool.cad.ci | **now in owner repo** | Complete tool.cad.ci #103 release + external acceptance, then qualify the released workflow in Forge. |
| #568 SolidCraft 0.45 sheet flange coverage parent | dev-cad | **tracking** | Coordinate #683 open chain and #684 contour flange; #682 is complete. |
| #683 Reusable open connected Sketch curve chains | dev-cad | **now** | Define requirements/design/API from pinned SolidCraft 0.45 line/tangent-arc contracts, then implement one focused qualification. |
| #684 Native contour flange | dev-cad | **blocked** | Implement only after #683 supplies the qualified open-chain contract. |
| #679 Namespace repeated component-local feature names | dev-cad | **next** | Audit after the active #683 slice unless it becomes a downstream blocker first. |
| #659 Standardize build/verification/results terminology | cross-repo | **later** | Start after #674 shared-governance extraction. |
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

## Recently completed

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
