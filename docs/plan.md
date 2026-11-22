# Forge repository plan

This file is the current source of truth for unfinished work in
`lib.py.solidcraft.forge`.

Forge is the central CAD library: public API, compiler/lowering, modelling
semantics, reusable CAD capabilities, examples and Forge-owned verification
expectations. Generic CAD-CI, generic CAD verification and runtime packaging
remain owned by their dedicated repositories.

## Current accepted baseline

Permanent source refs:

```text
main
dev-cad
dev-ci
```

Current stable `main` head:

`014de6446bf73dfabb2661df25161131e44e1bef`

Current accepted `dev-cad` head:

`3c692f3ce73d253892d1befee7ffb635b3169863`

Current `dev-ci` head:

`4f5ab5e403602d534c5044f38365cb1437709a74`

`dev-ci` has no unique source work relative to current `main`. The coherent
post-v0.11 CAD-library batch is on `dev-cad`.

### Forge release

Current real package release: **v0.11.0** at
`9258d54079981604b6dd777a4c4face897c190fe`.

Issue #714 is the explicit v0.12.0 release gate. No package version or dated
0.12.0 changelog section is prepared until the accepted CAD batch reaches
`main` and durable main/Pages provenance is green.

### Generic CAD-CI/merge stack

Library:

- `lib.py.cad.ci 0.11.0` @
  `e621daf6e309bdd0e3f643a12007f1b66490696d`.

Shared tool policy now available and externally accepted:

- `tool.cad.ci 0.20.0` @
  `d45cdcef33cf1035311bab9a88c3f99208ef3b29`;
- `tool.cad.ci.test` #82 / PR #83;
- external acceptance run `45031453651` — complete success;
- accepted test-repository main commit
  `125e19b95c6cf4892f5d65aa6162cf71d4f89c57`.

Forge still consumes 0.19.0 until #718 is merged. #718 is therefore the current
repository gate.

## Lane and merge rule

- `main`: stable integration only.
- `dev-cad`: Forge API/compiler/model/Verification/site-content work.
- `dev-ci`: CI/runtime/publication integration.
- Short-lived branches are squash-merged.
- Exact configured `dev-cad|dev-ci -> main`: normal merge promotion.
- Exact `main -> dev-cad|dev-ci`: normal merge synchronization.
- Both permanent-direction operations use only the exact released shared
  `/merge` policy and preserve permanent refs.
- Generic CI/verification/runtime behavior is fixed/released in its owner repo
  before Forge adopts it.

## Active workstreams

### WS1 — tool 0.20.0 adoption and branch reconciliation

Status: **now**.

1. #718 — adopt exact externally accepted tool.cad.ci 0.20.0 in the thin Forge
   wrapper and contract test.
2. #717 — after #718, perform the real history-preserving `main -> dev-cad`
   synchronization and require durable lane integration.
3. #716 / #714 — re-evaluate exact `dev-cad -> main` promotion; require fresh
   exact-head validation and merge only through `/merge`.
4. Verify durable `build/main` and stable Pages at the exact promoted main SHA.
5. Prepare and publish Forge v0.12.0 only through #714's explicit release gate.

PR #716 remains open and currently conflicted. Do not replace it with a
temporary promotion branch or squash the long-lived lane.

### WS2 — deferred repository/verification cleanup

- #713 scripts ownership audit — **later**. Do not resume during the active
  release/promotion path.
- #659 build/verify/results terminology — **later**.
- #570 remove CADCraft from Verification diagrams — **later**.
- #335 build123d sheet-metal reference semantics — **later**.

### WS3 — API coverage and research

- #349 remaining SOLID › CREATE coverage — **later**.
- #347 generalized pattern seeds — **later**.
- #325 AnchorFrame root-cause research — **later**.
- #81 rotated occurrence-local AnchorFrame references — **later**.
- #82 Joints-folder visibility — **later**.
- #9 first-class Sketch/constraints/workplanes — **later**.
- #8 hollow primitive intent — **later**.
- #175 — **probably obsolete**; consolidate useful evidence into #325.
- #5 — **probably obsolete** in current broad form; separate remaining
  constraint scope from #9.

## Open issue assignment — 2026-11-22

| Issue | Owner/lane | Status | Next action |
| --- | --- | --- | --- |
| #718 Adopt tool.cad.ci 0.20.0 | governance/main | **now** | Repin thin wrapper + contract to exact externally accepted release, then qualify and merge through current `/merge`. |
| #717 Reconcile main/dev-cad history | repository/dev-cad | **blocked on #718** | After adoption, execute history-preserving `main -> dev-cad` and require lane integration. |
| #714 Release Forge 0.12.0 | repository | **blocked on #717** | Resume #716 promotion, durable main/Pages verification, then explicit release preparation/publication. |
| #713 Audit/reduce Forge scripts | repository / verification owner | **later** | Reassess after the release checkpoint; do not interrupt WS1. |
| #659 Standardize build/verification/results terminology | cross-repo | **later** | Schedule separately after the release checkpoint. |
| #570 Remove CADCraft from Verification diagrams | dev-cad | **later** | Preserve diagram responsibility while replacing CADCraft sources. |
| #349 Remaining SOLID › CREATE coverage | dev-cad | **later** | Split focused work only when a current model requires it. |
| #347 Patterns accept any applied Shape feature | dev-cad | **later** | Generalize seed validation by native feature identity. |
| #335 build123d Sheet Metal reference | dev-cad | **later** | Replace the solid approximation with an actual sheet-metal reference workflow. |
| #325 AnchorFrame regression root cause | dev-cad | **later** | Resume when it becomes an active model dependency. |
| #175 HUB75-like AnchorFrame diagnostic | dev-cad | **probably obsolete** | Consolidate useful evidence into #325, then close or rewrite. |
| #82 Joints folder visibility | dev-cad | **later** | Decide interaction/export policy later. |
| #81 Inline rotated AnchorFrame references | dev-cad | **later** | Investigate with #325. |
| #9 First-class Sketch/constraints/workplanes | dev-cad | **later** | Refresh epic and deliver focused slices. |
| #8 Tube/RectTube/OvalTube | dev-cad | **later** | Reconcile intent with native shell/pipe/boolean histories. |
| #5 Generic anchors/parametric constraints | dev-cad | **probably obsolete** | Separate remaining constraint scope from overlap with #9. |

## Recently completed

- #679 component-local Sketch namespacing — exact-head PR run
  `45029824977`, merged to `dev-cad` as `35d0f558...`, durable lane run
  `45030057045` green.
- #703 canonical reusable `model.yml` contract — PR #711 merged to
  `dev-cad` as `45b0f52b...`.
- #684 native contour flange and #568 SolidCraft 0.45 flange parent — complete.
- #674 initial shared merge/lane policy adoption — tool 0.19.0 accepted and both
  short-lived squash and lane-to-main promotion paths qualified.
- #683 reusable open connected Sketch chains — merged and natively qualified.
- #682 native sheet edge flange — merged and natively qualified.
- #567 mixed line/arc profiles — merged and qualified.

## Next release checkpoint

Finish #718 -> #717 -> #716/#714 in that order. Do not accumulate another
CAD/API batch before v0.12.0 is either published or explicitly deferred.
