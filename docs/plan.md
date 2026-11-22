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

`4f5ab5e403602d534c5044f38365cb1437709a74`

Accepted post-v0.11 integration now includes:

- #354 standalone Sketch Boolean operands;
- #261 dependency-output `copy:` integration and jobs=2 runtime reduction;
- #662 durable workflow cut-over to one released same-runner action;
- durable `build/main` and stable Pages provenance through the released shared policy on exact `4f5ab5e4...`;
- #674 shared merge/lane policy adoption, including live short-lived squash/cleanup and exact permanent-lane normal-merge qualification.

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
  `45022699789` — success for tool 0.19.0, including the released merge-policy contract.

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
| `model-verification-batch` | **current; selective context accepted** | #661/#688 proved one-model, no-op and explicit full-run behavior on the released active-dependent contract. |
| `reference-verification-batch` | **current** | Shared heavy reference runtime for independent CAD implementations and diagram production. |
| `release-policy` | **current** | Tests release validator/publisher without CAD runtimes and is an explicit release gate. |
| `site-source` | **current** | Keeps presentation/source validation independent from CAD execution. |
| `solidcraft-reference` | **current; low-frequency guard** | Verifies the checked SolidCraft command registry against the immutable runtime. |
| `verification-diagrams` | **current; implementation transition planned** | Public/site diagram evidence is still consumed; #570 removes CADCraft while preserving the diagram responsibility. |

Do not remove or combine an item merely to reduce directory count. Any future
structural simplification needs a separate requirements/design decision after
the current responsibilities and consumers remain preserved.

### WS1 — shared merge/lane policy adoption — complete

The generic owner/release and both Forge live paths are accepted:

- `tool.cad.ci 0.19.0` @ `5677c41a61929b32ab2cb07087a6505f7b9347d8`;
- external acceptance: `tool.cad.ci.test` run `45022699789`;
- short-lived path: #696 / PR #697 proved squash merge, allow-listed temporary branch cleanup and dispatched `dev-ci` integration;
- direct lane path: PR #702 was exactly `dev-ci -> main`; policy run `45027212738` produced normal two-parent merge `4f5ab5e403602d534c5044f38365cb1437709a74`, preserved the permanent `dev-ci` lane and dispatched successful `main` and `dev-ci` integrations `45027231104` and `45027232676`;
- #674 and preparation child #699 are closed.

No Forge-local merge-policy fallback remains. Future merges use only the released shared `/merge` policy.
### WS2 — active CAD-library lane

Primary lane: `dev-cad`.

- #567 mixed line/arc closed Sketch profiles — **complete**.
- #682 native `sheet.flange(type=edge)` — **complete**.
- #683 reusable open connected Sketch chains — **complete**; PR #694, native batch `45025059775` and lane integration `45025329364` are green.
- #684 native `sheet.flange(type=contour)` — **effectively complete but still open** in draft PR #698; native qualification run `45027053821` is green and the final one-commit head check is the remaining merge gate.
- #568 remains the active tracking parent for the SolidCraft 0.45 flange family.
- #679 component-local feature-name namespacing — **next** after #684 unless downstream CAD makes it the immediate blocker.
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
| #568 SolidCraft 0.45 sheet flange coverage parent | dev-cad | **now** | Track #684 through merge/lane integration; then reassess whether the flange family has unfinished child scope. |
| #684 Native contour flange | dev-cad | **effectively complete but still open** | Final one-commit PR #698 head check, `/merge`, then require successful dispatched `dev-cad` integration before closure. |
| #679 Namespace repeated component-local feature names | dev-cad | **next** | Resume after #684 unless downstream HUB75 work makes it the immediate blocker. |
| #659 Standardize build/verification/results terminology | cross-repo | **later** | Governance is stable; schedule separately so terminology work does not mix with active #684/#679 CAD changes. |
| #349 Remaining SOLID › CREATE coverage | dev-cad | **later** | Split focused Revolve child for latch work. |
| #570 Remove CADCraft from Verification diagrams | dev-cad | **later** | Replace explanatory sources without moving generic rendering into Forge. |
| #335 build123d Sheet Metal reference | dev-cad | **later** | Replace the solid approximation with actual sheet-metal workflow. |
| #347 Patterns accept any applied Shape feature | dev-cad | **later** | Generalize seed validation by native feature identity. |
| #325 AnchorFrame regression root cause | dev-cad | **later** | Resume only when it becomes an active dependency. |
| #81 Inline rotated AnchorFrame references | dev-cad | **later** | Investigate occurrence-local frames with #325. |
| #82 Joints folder visibility | dev-cad | **later** | Decide interaction/export policy later. |
| #9 First-class Sketch/constraints/workplanes | dev-cad | **later** | Refresh epic and deliver focused slices. |
| #8 Tube/RectTube/OvalTube | dev-cad | **later** | Reconcile intent with native shell/pipe/boolean histories. |
| #175 HUB75-like AnchorFrame diagnostic | dev-cad | **probably obsolete** | Consolidate useful evidence into #325, then close/rewrite. |
| #5 Generic anchors/parametric constraints | dev-cad | **probably obsolete** | Separate remaining constraint scope from overlap with #9. |
## Recently completed

- #674 shared merge/lane policy adoption — released owner workflow adopted and both live merge paths qualified; PR #702 promoted `dev-ci -> main` as normal merge `4f5ab5e4...` with both dispatched lane integrations green.
- #699 promotion-plan preparation — completed before the exact lane promotion.
- #696 / PR #697 shared-policy short-lived canary — squash, temporary-head cleanup and dispatched `dev-ci` integration proven.
- #683 reusable open connected Sketch chains — merged and natively qualified on `dev-cad`.
- #567 connected mixed line/arc profiles — merged and qualified on `dev-cad`.
- #682 native sheet edge flange — merged and qualified on `dev-cad`.
- #661/#688 selective shared model batch — complete; one-model, no-op and
  full-promotion evidence accepted and promoted to main.
- tool.cad.ci 0.19.0 merge-policy owner/release acceptance — complete and consumed by Forge #674.

## Next release checkpoint

Before a second large post-v0.11 batch accumulates, open the planned v0.12.0
release issue and explicitly include/defer the merged CAD/CI work. Do not bump
source metadata before that release gate exists.
