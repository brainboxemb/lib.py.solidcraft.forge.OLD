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
| `model-verification-batch` | **current; selective consumer context accepted** | Shared SolidCraft runtime remains desired; #661 now restricts the producer to CAD-CI active direct model dependents. |
| `reference-verification-batch` | **current** | Shared heavy reference runtime for independent CAD implementations and diagram production. |
| `release-policy` | **current** | Tests release validator/publisher without CAD runtimes and is an explicit release gate. |
| `site-source` | **current** | Keeps presentation/source validation independent from CAD execution. |
| `solidcraft-reference` | **current; low-frequency guard** | Verifies the checked SolidCraft command registry against the immutable runtime. |
| `verification-diagrams` | **current; implementation transition planned** | Public/site diagram evidence is still consumed; #570 removes CADCraft while preserving the diagram responsibility. |

Do not remove or combine an item merely to reduce directory count. Any future
structural simplification needs a separate requirements/design decision after
the current responsibilities and consumers remain preserved.

### WS1 — #674 shared merge/lane policy extraction

Primary lane: `dev-ci`. **Next.**

Forge currently carries a repository-local implementation of the reusable
main/dev-cad/dev-ci merge policy. Downstream CAD now needs the same mechanical
behavior.

#674 is a Forge consumer/qualification requirement, not permission to duplicate
the implementation again. Before changing Forge:

1. record the exact current Forge merge/lane behavior that must be preserved;
2. open/use the normative implementation issue in the actual shared owner
   (expected `tool.cad.ci` unless the owner audit says otherwise);
3. test and release the shared implementation there;
4. externally accept that exact release;
5. replace Forge-local policy only after released equivalence is demonstrated.

The temporary CAD-local copy must not block current CAD migration and must not
be treated as the final architecture.

### WS2 — native sheet-metal CAD-library work

Primary lane: `dev-cad`. **Now, independent of dev-ci.**

#567 connected mixed line/arc closed profiles is complete and merged. #568 is
now only the SolidCraft 0.45 flange-family tracking parent.

Current focused children:

- #682 native `sheet.flange(type=edge)` — **now**;
- #683 reusable open connected Sketch curve chains — **next**;
- #684 native `sheet.flange(type=contour)` — **blocked on #683**;
- #349 focused Revolve child first — **later**.

Do not recombine #682/#683/#684 into one broad sheet-metal change.

### WS4 — cross-repository terminology and Verification/reference quality

- #659 build/verify/results terminology — **later**; start after the active #674 governance extraction so architecture and vocabulary do not move together.
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
| #674 Shared merge/lane policy extraction | dev-ci / shared owner | **next** | Preserve current Forge behavior as consumer acceptance, implement/release in the actual shared owner, then replace Forge-local policy only after equivalence. |
| #568 SolidCraft 0.45 sheet flange coverage parent | dev-cad | **tracking** | Coordinate #682/#683/#684 only; no direct implementation PR. |
| #682 Native sheet edge flange | dev-cad | **now** | Complete focused native qualification for the documented minimal edge-flange slice. |
| #683 Reusable open connected Sketch curve chains | dev-cad | **next** | Design/qualify generic open line+tangent-arc chain after #682. |
| #684 Native contour flange | dev-cad | **blocked** | Implement only after #683 supplies the qualified open-chain contract. |
| #679 Namespace repeated component-local feature names | dev-cad | **next** | Audit as reusable Forge compiler requirement; keep separate from sheet-metal work. |
| #659 Standardize build/verification/results terminology | cross-repo | **later** | Start after #674 shared-governance architecture is settled. |
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

- #670 CI/scripts documentation — central and per-item CI documentation merged to `dev-ci`.
- #661 selective shared model batch — merged Forge adoption of tool.cad.ci 0.18.1 / lib.py.cad.ci 0.11.0; one-model proof run `45021406133` executed only `simple-box` in one shared SolidCraft container (batch total ~10.9 s), while explicit full-run behavior remains complete.
- #567 mixed line/arc closed Sketch profiles — merged to `dev-cad` with native saved-design qualification.

## Next release checkpoint

Before a second large post-v0.11 batch accumulates, open the planned v0.12.0
release issue and explicitly include/defer the merged CAD/CI work. Do not bump
source metadata before that release gate exists.
