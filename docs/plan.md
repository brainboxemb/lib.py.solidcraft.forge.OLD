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

Current stable `main` head:

`014de6446bf73dfabb2661df25161131e44e1bef`

Current accepted `dev-cad` head:

`35d0f55819e28d5eeab3ec712f1975d2df91e0a3`

Current `dev-ci` head:

`4f5ab5e403602d534c5044f38365cb1437709a74`

`dev-ci` has no unique source work relative to current `main`. The coherent
post-v0.11 CAD-library batch is on `dev-cad`.

The accepted `dev-cad` head has:

- exact-head PR qualification for #679 in run `45029824977`;
- policy-dispatched durable lane integration run `45030057045` — success;
- matching `build/dev-cad/build.json` provenance at `35d0f558...`;
- successful matching `/dev-cad/` Pages publication.

### Forge release

Current real package release: **v0.11.0** at
`9258d54079981604b6dd777a4c4face897c190fe`.

Issue #714 is the explicit **v0.12.0** release gate. Do not bump package
metadata or create a dated 0.12.0 changelog section before the `dev-cad -> main`
promotion is accepted and one exact release candidate is chosen.

### SolidCraft runtime

- `docker.cad.solidcraft v0.3.4`;
- `cad-solidcraft:v0.3.4`;
- `cad-reference:v0.3.4`;
- SolidCraft CLI `0.45.0`.

### Accepted generic CAD-CI stack

- `lib.py.cad.ci 0.11.0`;
- `tool.cad.ci 0.19.0`;
- external acceptance in `tool.cad.ci.test` is green;
- Forge consumes the released shared merge policy and durable same-runner path.

Forge remains explicitly on `jobs=2` and does not duplicate generic planning,
build-store publication, merge-policy or runtime packaging logic.

## Lane rule

- `main`: stable integration only.
- `dev-cad`: Forge API/compiler/model/Verification/site-content behavior.
- `dev-ci`: CAD-CI/runtime/publication integration.
- Generic CI behavior is fixed and released in `lib.py.cad.ci` /
  `tool.cad.ci` first.
- Generic Verification behavior is fixed and released in
  `lib.py.cad.verification` first.
- Runtime packaging is fixed and released in `docker.cad.solidcraft` first.

Short-lived branches target one lane and are squash-merged through `/merge`.
Exact `dev-cad -> main` and `dev-ci -> main` promotions use the same released
policy and therefore receive normal merge commits. Do not introduce a temporary
promotion branch.

## Active workstreams

### WS1 — v0.12.0 integration and release

Owner: Forge repository; issue #714.

Status: **now**.

Completed post-v0.11 CAD-library scope on `dev-cad` includes:

- #567 connected mixed line/arc Sketch profiles;
- #682 native sheet edge flange;
- #683 reusable open connected Sketch chains;
- #684 native contour flange;
- #703 canonical reusable `model.yml` contract;
- #679 component-local native Sketch feature namespacing.

#679 is complete after PR #712, exact-head run `45029824977`, squash merge
`35d0f558...` and durable lane integration run `45030057045`.

Next gate:

1. promote exact `dev-cad -> main` through a direct PR;
2. require the PR to qualify the complete combined main + CAD history;
3. merge only through `/merge`, which must select a normal merge commit for
   the exact permanent-lane promotion;
4. verify the resulting exact `main` SHA has successful durable
   `build/main` and stable Pages provenance;
5. only then prepare the explicit v0.12.0 candidate under #714;
6. publish only through `/release v0.12.0 <exact-main-sha>` after
   `forge-release`, `release-policy`, durable build and Pages all agree.

If the direct lane PR exposes a real overlap between main-side governance and
CAD-lane documentation, reconcile that overlap explicitly before merge. Do not
replace the direct permanent-lane promotion with a squash workaround.

### WS2 — deferred repository/verification cleanup

- #713 scripts ownership audit — **later**. Do not interrupt the active v0.12.0
  promotion/release path. Reassess its wording against the current
  `scripts/README.md` before implementation.
- #659 build/verify/results terminology — **later**.
- #570 remove CADCraft from Verification diagrams — **later**.
- #335 build123d sheet-metal reference semantics — **later**.

### WS3 — API coverage and interaction research

- #349 remaining SOLID › CREATE coverage — **later**; split focused Revolve work
  when a current model requires it.
- #347 generalized pattern seeds — **later**.
- #9 first-class Sketch/constraints/workplanes — **later** epic.
- #8 hollow primitive intent — **later**.
- #325 AnchorFrame root-cause research — **later**.
- #81 rotated occurrence-local AnchorFrame references — **later**.
- #82 Joints-folder visibility — **later**.
- #175 — **probably obsolete**; consolidate useful evidence into #325.
- #5 — **probably obsolete** in current broad form; separate remaining
  constraint scope from #9.

## Open issue assignment — 2026-11-22

| Issue | Lane/owner | Status | Next action |
| --- | --- | --- | --- |
| #714 Release Forge 0.12.0 | repository | **now** | Directly promote accepted `dev-cad` to `main`, verify durable main/Pages, then prepare and publish one exact v0.12.0 candidate. |
| #713 Audit/reduce Forge scripts | repository / verification owner | **later** | Reassess current tree/documentation after the release; do not resume the audit during the active promotion. |
| #659 Standardize build/verification/results terminology | cross-repo | **later** | Schedule separately after the release checkpoint. |
| #570 Remove CADCraft from Verification diagrams | dev-cad | **later** | Preserve diagram responsibility while replacing CADCraft sources. |
| #349 Remaining SOLID › CREATE coverage | dev-cad | **later** | Split a focused child when a current model needs one of the remaining creators. |
| #347 Patterns accept any applied Shape feature | dev-cad | **later** | Generalize seed validation by native feature identity. |
| #335 build123d Sheet Metal reference | dev-cad | **later** | Replace the solid approximation with an actual sheet-metal reference workflow. |
| #325 AnchorFrame regression root cause | dev-cad | **later** | Resume when it becomes an active model dependency. |
| #175 HUB75-like AnchorFrame diagnostic | dev-cad | **probably obsolete** | Consolidate useful evidence into #325, then close or rewrite. |
| #82 Joints folder visibility | dev-cad | **later** | Decide interaction/export policy later. |
| #81 Inline rotated AnchorFrame references | dev-cad | **later** | Investigate together with #325. |
| #9 First-class Sketch/constraints/workplanes | dev-cad | **later** | Refresh the epic and deliver focused slices. |
| #8 Tube/RectTube/OvalTube | dev-cad | **later** | Reconcile hollow-primitive intent with native shell/pipe/boolean histories. |
| #5 Generic anchors/parametric constraints | dev-cad | **probably obsolete** | Separate remaining constraint scope from overlap with #9. |

## Recently completed

- #679 component-local Sketch namespacing — PR #712 merged to `dev-cad` as
  `35d0f558...`; PR run `45029824977` and durable lane run `45030057045`
  succeeded.
- #703 canonical reusable `model.yml` contract — PR #711 merged to
  `dev-cad` as `45b0f52b...` after exact-head run `45029270620`.
- #684 native contour flange and #568 SolidCraft 0.45 flange tracking parent —
  complete after exact-head lane integration run `45027571753`.
- #674 shared merge/lane policy adoption — released owner workflow adopted and
  both short-lived and permanent-lane paths qualified.
- #683 reusable open connected Sketch chains — merged and natively qualified.
- #682 native sheet edge flange — merged and natively qualified.
- #661/#688 selective shared model batch — accepted and promoted through
  `dev-ci -> main`.
- #567 mixed line/arc closed Sketch profiles — merged and qualified.

## Next release checkpoint

Issue #714 is the active checkpoint.

The next source transition is the direct `dev-cad -> main` promotion. After
that exact main integration is green, prepare v0.12.0 deliberately; do not
continue accumulating another large CAD/API batch before the release decision.
