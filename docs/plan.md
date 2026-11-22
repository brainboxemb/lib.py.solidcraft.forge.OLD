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

`1689ddbc478a80f0b036da7868d29b15d6aef8e3`

Current accepted `dev-cad` head:

`8ee6c3f4df624ba437c8c370a565bd92b62ef8fa`

Current `dev-ci` head:

`4f5ab5e403602d534c5044f38365cb1437709a74`

`dev-ci` has no unique source work relative to current `main`.

`dev-cad` is intentionally in a temporary merge-neutral documentation state
under #722. The complete pre-neutralization CAD documentation is preserved at
`f4440ec2c1f2e80e084f0bd94fd51afc1d452271` and must be restored after the
history synchronization succeeds.

### Forge release

Current real package release: **v0.11.0** at
`9258d54079981604b6dd777a4c4face897c190fe`.

Issue #714 is the explicit v0.12.0 release gate. No package version or dated
0.12.0 changelog section is prepared until the accepted CAD batch reaches
`main`, durable main/Pages provenance is green, and #722 documentation
restoration is complete.

### Generic CAD-CI/merge stack

Library:

- `lib.py.cad.ci 0.11.0` @
  `e621daf6e309bdd0e3f643a12007f1b66490696d`.

Current released and externally accepted merge tool:

- `tool.cad.ci 0.20.1` @
  `eb64a46b243db00e8dbb4b78b6643a2a7efa3fb9`;
- `tool.cad.ci.test` #84 / PR #85;
- full external acceptance run `45033890474` — success;
- accepted test-repository main commit
  `d01153ceed336ab76d4385ddc1f4a2d462c73103`.

Forge still consumes 0.20.0 until #726 is merged. #726 is therefore the active
owner-release adoption gate.

## Lane and merge rule

- `main`: stable integration only.
- `dev-cad`: Forge API/compiler/model/Verification/site-content work.
- `dev-ci`: CI/runtime/publication integration.
- Short-lived branches are squash-merged.
- Exact configured `dev-cad|dev-ci -> main`: normal merge promotion.
- Exact `main -> dev-cad|dev-ci`: normal merge synchronization.
- Both permanent-direction operations use only the exact released shared
  `/merge` policy and preserve permanent refs.
- Same-head `issue_comment` command workflows are not PR validation checks;
  tool.cad.ci 0.20.1 filters those command checks by Actions-run identity while
  still requiring normal validation/status gates.
- Generic CI/verification/runtime behavior is fixed/released in its owner repo
  before Forge adopts it.

## Active workstreams

### WS1 — finish history reconciliation and v0.12.0 promotion

Status: **now**.

Current evidence:

- exact sync PR #721 (`main -> dev-cad`) is clean/mergeable;
- full exact-head validation run `45032993674` succeeded;
- the 0.20.0 `/merge` attempt was refused only because the command workflow
  saw its own `merge / merge=in_progress` check on the stable head;
- generic fix #108 is released as tool.cad.ci 0.20.1 and externally accepted.

Required order:

1. #726 — adopt exact externally accepted tool.cad.ci 0.20.1 in Forge.
2. Refresh #721 against the resulting main head and mirror only any newly
   changed shared plan/changelog text to the temporary merge-neutral
   `dev-cad` state if needed.
3. Require fresh exact-head validation for #721 and merge it through `/merge`;
   verify a real normal two-parent stable-to-lane merge, unchanged `main` and
   successful durable `dev-cad` integration.
4. #722 — restore dev-cad-only CAD documentation from exact snapshot
   `f4440ec2...`, reconcile the plan, qualify, merge and require durable lane
   integration.
5. Close #722 and #717 only after that restoration is accepted.
6. #716 / #714 — refresh exact `dev-cad -> main` promotion, require fresh
   exact-head validation and merge only through `/merge`.
7. Verify durable `build/main` and stable Pages at the exact promoted main SHA.
8. Prepare and publish Forge v0.12.0 only through #714's explicit release gate.

PR #716 remains open. Do not replace either permanent-direction PR with a
temporary promotion/synchronization branch.

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
| #733 Align handoff markup with shared template | governance/main | **now** | Add the explicit handoff-message section/copy instruction required by the accepted meta template. |
| #726 Adopt tool.cad.ci 0.20.1 | governance/main | **now** | Repin only the thin wrapper/test to the exact externally accepted patch release; qualify and merge through shared policy. |
| #722 Normalize/restore shared documents around sync | dev-cad | **blocked on #721** | Temporary merge-neutral state is complete; after successful sync, restore CAD documentation from exact `f4440ec2...`. |
| #717 Reconcile main/dev-cad history | repository/dev-cad | **blocked on #726** | Refresh and retry exact PR #721 with 0.20.1, then require durable lane integration and #722 restoration. |
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

- #729 moved the canonical Forge session handoff to `docs/handoff.md`, retired the old manual copy and aligned the document with the shared meta handoff template.
- tool.cad.ci #108 — 0.20.1 released at `eb64a46b...`; external acceptance
  run `45033890474` succeeded.
- #722 pre-sync conflict neutralization — dev-cad now at `8ee6c3f4...`; all
  five known conflict documents were made merge-neutral for #721.
- #718 tool.cad.ci 0.20.0 adoption — PR #719 run `45031935896` green; merged
  as `4b1af992...`; durable main/Pages run `45032014292` green.
- #679 component-local Sketch namespacing — exact-head PR run
  `45029824977`, merged to `dev-cad` as `35d0f558...`, durable lane run
  `45030057045` green.
- #703 canonical reusable `model.yml` contract — PR #711 merged to
  `dev-cad` as `45b0f52b...`.
- #684 native contour flange and #568 SolidCraft 0.45 flange parent — complete.
- #683 reusable open connected Sketch chains — merged and natively qualified.
- #682 native sheet edge flange — merged and natively qualified.
- #567 mixed line/arc profiles — merged and qualified.

## Next release checkpoint

Finish #726 -> #721/#717 -> #722 restoration -> #716/#714 in that order. Do not
accumulate another CAD/API batch before v0.12.0 is either published or explicitly
deferred.
