# Forge repository plan

This file is the current source of truth for unfinished work in
`lib.py.solidcraft.forge`.

Forge is first and foremost the central CAD library: public API, compiler/lowering,
modelling semantics, reusable CAD capabilities, examples and Forge-owned verification
expectations. Generic CAD-CI, generic CAD verification and runtime packaging remain
owned by their dedicated repositories and are consumed here only as released
dependencies.

`dev-cad` and `dev-ci` advance independently unless they share a real owner
release or architecture gate.

## Current accepted baseline

Permanent source lanes:

```text
main
dev-cad
dev-ci
```

Current stable integration commit on `main`:

`66cdc5bd832bd21fc5c1275d9a8b0929790a1a90`

Current `dev-cad` head:

`2fc5cc8cf01809fed6317ca0b90c5b94d890e2fe`

Accepted post-v0.11 integration includes the released shared merge/lane policy on
`main`; the active CAD lane additionally contains the completed native SolidCraft
0.45 edge-flange, open-chain and contour-flange slices.

### Forge release

Current package release: **v0.11.0** at
`9258d54079981604b6dd777a4c4face897c190fe`.

New user-visible work remains under `[Unreleased]`. The next planned package
checkpoint is v0.12.0 after a coherent post-v0.11 CAD/CI batch reaches `main`.
Do not bump source metadata before an explicit release issue/gate exists.

### SolidCraft runtime

- docker.cad.solidcraft v0.3.4;
- cad-solidcraft:v0.3.4;
- cad-reference:v0.3.4;
- SolidCraft CLI 0.45.0.

### Accepted generic CAD-CI stack

- `lib.py.cad.ci 0.11.0`;
- `tool.cad.ci 0.19.0`;
- external acceptance in `tool.cad.ci.test` is green.

Forge remains explicitly on `jobs=2` and does not duplicate generic planning,
build-store publication, merge-policy or runtime packaging logic.

## Lane rule

- `dev-cad`: Forge API/compiler/model/Verification/site-content behavior.
- `dev-ci`: CAD-CI/runtime/publication integration.
- Generic CI behavior is fixed and released in `lib.py.cad.ci` /
  `tool.cad.ci` first.
- Generic Verification behavior is fixed and released in
  `lib.py.cad.verification` first.
- Runtime packaging is fixed and released in `docker.cad.solidcraft` first.

Short-lived branches target one lane and are squash-merged through `/merge`.
Exact `dev-cad -> main` and `dev-ci -> main` promotions use the same policy
and therefore receive normal merge commits.

## Active workstreams

### WS1 — active CAD-library lane

Primary lane: `dev-cad`.

- #684 native `sheet.flange(type=contour)` — **complete**; PR #698 merged to
  `dev-cad` as `2fc5cc8c...` and exact-head lane integration run
  `45027571753` succeeded.
- #568 SolidCraft 0.45 sheet-flange tracking parent — **complete**; #682, #683
  and #684 cover the identified flange-family scope.
- #679 component-local feature-name namespacing — **now**. Downstream shared-batch
  evidence already shows repeated reusable component feature names collide at
  SolidCraft document scope. Preserve component-local authoring semantics while
  lowering deterministic document-global identities.
- #703 canonical reusable `model.yml` contract — **next**. Forge already owns
  the human-facing metadata meaning; formalize one reusable schema/template and
  make consumers reuse it instead of maintaining a divergent validator.

### WS2 — cross-repository terminology and Verification/reference quality

- #659 build/verify/results terminology — **later**.
- #570 remove CADCraft from Verification diagrams — **later**.
- #335 build123d sheet-metal reference semantics — **later**.

### WS3 — API coverage and interaction research

- #349 remaining SOLID › CREATE coverage — **later**; split focused Revolve work
  when latch work requires it.
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
| #679 Namespace repeated component-local feature names | dev-cad | **now** | Update requirements/design for local-vs-document identity, then implement one focused lowering slice and qualification. |
| #703 Canonical reusable model.yml contract | dev-cad | **next** | Define the reusable human-facing metadata schema/template in Forge and an adoption contract for CAD consumers. |
| #659 Standardize build/verification/results terminology | cross-repo | **later** | Schedule separately from active CAD/compiler changes. |
| #349 Remaining SOLID › CREATE coverage | dev-cad | **later** | Split focused Revolve child when required. |
| #570 Remove CADCraft from Verification diagrams | dev-cad | **later** | Preserve diagram responsibility while replacing CADCraft sources. |
| #335 build123d Sheet Metal reference | dev-cad | **later** | Replace solid approximation with actual sheet-metal workflow. |
| #347 Patterns accept any applied Shape feature | dev-cad | **later** | Generalize seed validation by native feature identity. |
| #325 AnchorFrame regression root cause | dev-cad | **later** | Resume when it becomes an active dependency. |
| #81 Inline rotated AnchorFrame references | dev-cad | **later** | Investigate with #325. |
| #82 Joints folder visibility | dev-cad | **later** | Decide interaction/export policy later. |
| #9 First-class Sketch/constraints/workplanes | dev-cad | **later** | Refresh epic and deliver focused slices. |
| #8 Tube/RectTube/OvalTube | dev-cad | **later** | Reconcile intent with native shell/pipe/boolean histories. |
| #175 HUB75-like AnchorFrame diagnostic | dev-cad | **probably obsolete** | Consolidate useful evidence into #325, then close/rewrite. |
| #5 Generic anchors/parametric constraints | dev-cad | **probably obsolete** | Separate remaining constraint scope from overlap with #9. |

## Recently completed

- #684 native contour flange and #568 SolidCraft 0.45 flange tracking parent — complete after exact-head `dev-cad` integration run `45027571753` succeeded.
- #674 shared merge/lane policy adoption — released owner workflow adopted and
  live short-lived plus permanent-lane paths qualified.
- #683 reusable open connected Sketch chains — merged and natively qualified on
  `dev-cad`.
- #682 native sheet edge flange — merged and natively qualified on `dev-cad`.
- #661/#688 selective shared model batch — accepted and promoted through
  `dev-ci -> main`.
- #567 mixed line/arc closed Sketch profiles — merged and qualified.

## Next release checkpoint

Open the planned v0.12.0 release issue before a second large post-v0.11 batch
accumulates. Explicitly include or defer the merged CAD/CI work; do not create a
release implicitly from normal CI.
