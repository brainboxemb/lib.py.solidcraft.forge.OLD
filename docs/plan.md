# Forge repository plan

This file is the current source of truth for unfinished work in
`lib.py.solidcraft.forge`.

Forge owns the public CAD library/compiler/model semantics, Forge-specific
verification expectations, presentation policy and repository-specific builder
commands. Generic CAD-CI, reusable CAD verification, runtime packaging,
durable build state, Pages publication and merge governance stay in their owner
repositories.

## Current repository state

Permanent source refs:

```text
main
dev-cad
dev-ci
```

Current heads after the #721 history-preserving synchronization:

- `main`: `3f8811b6cc7174af64f0ce45aad890051e3ccc40`;
- `dev-ci`: `90ac473473ab954103190ba426b350852b380fc0`;
- `dev-cad`: `1a751317b8f1901118084ecc6e9f6faa9b1adf6b` before this
  documentation-restoration PR.

#740 is complete and closed. Stable CAD-CI is accepted on `main`; the later
`3f8811b...` main commit is the plan-only reconciliation after that accepted
cut-over.

#721 completed the required real two-parent `main -> dev-cad`
synchronization at `1a751317...`, with parents `eebff74...` and
`3f8811b...`. Durable dev-cad run `45227292709` is green, and
`build/dev-cad`, dev-cad Pages and Verification provenance all identify
`1a751317...`.

The active step is #722 phase B: restore only the preserved dev-cad CAD-library
documentation on top of the synchronized v0.35/main baseline. After the
restored lane is durable-green, #716 can resume as the exact
`dev-cad -> main` promotion for the v0.12.0 candidate.

### Forge package release

Current real Forge package release: **v0.11.0** at
`9258d54079981604b6dd777a4c4face897c190fe`.

Issue #714 remains the explicit v0.12.0 release gate. The dev-cad CAD/API batch
must not be promoted/released until the CI cut-over is stable, dev-cad history
is synchronized/restored and durable main/Pages evidence is green.

### Accepted generic owner stack

- `lib.py.cad.ci v0.18.2` @
  `088644a05ff698957aef2ddc6cc5de037ddfa158`;
- `tool.cad.ci v0.35.0` @
  `9fcad92b7c5f10ae29a9cb085a4f25bb38ed00f9`;
- `lib.py.cad.verification v0.16.0` @
  `c7c145b7be0c602724e8cca874ef29990baaad1e`;
- `docker.cad.solidcraft v0.3.4` immutable SolidCraft/reference runtimes;
- v0.34.2/v0.18.2 CadQuery Workplane + Assembly acceptance and permanent-lane
  durable provenance completed in `tool.cad.ci.test #248`;
- v0.35.0 targeted `item` + multi-path workflow selection completed in
  `tool.cad.ci.test #254`.

## Permanent branch rule

- `main`: stable integration only.
- `dev-cad`: Forge API/compiler/model/Verification/site-content work.
- `dev-ci`: CI/runtime/publication integration.
- short-lived branches are squash-merged;
- exact `dev-cad|dev-ci -> main`: history-preserving normal merge;
- exact `main -> dev-cad|dev-ci`: history-preserving normal merge;
- merge mechanics come only from the exact released shared policy;
- generic CI/verification/runtime behavior is changed/released in the owner repo
  before Forge adopts it.

## Active workstreams

### WS1 — reconcile dev-cad history and Forge v0.12.0

Status: **now**. The #740 stable cut-over is complete.

Required order:

1. **complete** — #722 phase A mirrored the final stable shared documents;
2. **complete** — #721 / #717 synchronized exact `main -> dev-cad` as a
   two-parent merge and durable dev-cad evidence is green;
3. **now** — #722 phase B restores the preserved dev-cad-only CAD
   documentation without restoring retired CI/governance text;
4. after restored dev-cad durable evidence is green, resume #716 exact
   `dev-cad -> main` promotion;
5. #714 prepares/publishes Forge v0.12.0 through the explicit release gate.

### WS2 — subsequent infrastructure/documentation work

- #739 released `tool.py.lib.ci` release-template adoption — **after the
  current dev-cad/v0.12 checkpoint**. Do not move `main` again while #722/#721
  are establishing the final merge base.
- #713 scripts ownership audit — **later**, but #740 may delete scripts that
  become unambiguously obsolete because owner functionality has replaced them.
- #737 historical changelog normalization — **later / docs-only**.
- #659 build/verification/results terminology — **later**.
- #570 CADCraft diagram replacement — **later**.
- #335 build123d Sheet Metal reference semantics — **later**.

### WS3 — CAD/API work after the release checkpoint

Issues #746, #747, #748, #749, #750, #751 and #753 are real reusable Forge
gaps but are **blocked on the current dev-cad history/v0.12 checkpoint**.
#753 already has draft PR #754 as a focused native qualification fixture; keep
it draft and do not merge it before the checkpoint. Do not accumulate another
CAD/API release batch before v0.12.0 is either published or explicitly deferred.

Other longer-term API/research work remains later: #349, #347, #325, #81, #82,
#9 and #8. #175 and #5 remain probably obsolete in their current broad forms.

## Open issue assessment — 2026-11-23

| Issue | Owner/lane | Status | Next action |
| --- | --- | --- | --- |
| #739 Adopt tool.py.lib.ci release template | dev-ci | **blocked on v0.12 checkpoint** | Keep separate and avoid moving main again during #722/#721/#716 history reconciliation. |
| #722 Normalize/restore shared docs around dev-cad sync | dev-cad | **now** | Phase A and #721 are complete; restore only preserved CAD-library docs on the synchronized baseline, then require restored dev-cad durable green and close #722. |
| #717 Reconcile main/dev-cad history | dev-cad | **effectively complete but still open** | #721 is a verified two-parent sync and durable evidence is green; close after #722 restoration proves the final dev-cad lane and #716 re-evaluates cleanly. |
| #714 Release Forge 0.12.0 | repository | **blocked on #717/#716** | Prepare/publish only after promoted main and durable evidence are green. |
| #746 Cone join/cut feature compilation | dev-cad | **blocked on v0.12 checkpoint** | Reusable compiler gap; implement in the next CAD/API batch. |
| #747 Polygon2D explicit/attached Sketch compilation | dev-cad | **blocked on v0.12 checkpoint** | Required by downstream CAD; no consumer workaround. |
| #748 Qualified STL export path | dev-cad/runtime owner | **blocked on v0.12 checkpoint** | Determine native export owner, then qualify released path. |
| #749 Isolate project-local modules between run_script roots | dev-cad | **blocked on v0.12 checkpoint** | Fix runner ownership, no consumer sys.modules workaround. |
| #750 Standalone Shape local transform/rotation | dev-cad | **blocked on v0.12 checkpoint** | Add generic cutter transform support after release checkpoint. |
| #751 Native SolidCraft exploded views | dev-cad | **blocked on v0.12 checkpoint** | Wrap/qualify native explode API after release checkpoint. |
| #753 Qualify component-local native Cylinder joins across copied/rotated occurrences | dev-cad | **blocked on v0.12 checkpoint** | Draft PR #754 exists; retain it as the focused runtime/Forge qualification fixture and resume after the history/release checkpoint. |
| #713 Audit/reduce Forge scripts | repository | **later** | Reassess after #740/#714; remove only genuine duplicates. |
| #737 Historical changelog alignment | docs | **later** | Do not mix retrospective rewrite into CI/release cut-over. |
| #659 Standardize build/verification/results terminology | cross-repo | **later** | Separate follow-up. |
| #570 Remove CADCraft from Verification diagrams | dev-cad | **later** | Preserve presentation responsibility while replacing source format. |
| #349 Remaining SOLID › CREATE coverage | dev-cad | **later** | Focused slices only when needed. |
| #347 Generalized pattern seeds | dev-cad | **later** | Generalize by native feature identity. |
| #335 build123d Sheet Metal reference | dev-cad | **later** | Replace solid approximation with real sheet-metal reference. |
| #325 AnchorFrame root cause | dev-cad | **later** | Resume when an active model requires it. |
| #175 HUB75-like AnchorFrame diagnostic | dev-cad | **probably obsolete** | Consolidate useful evidence into #325. |
| #82 Joints-folder visibility | dev-cad | **later** | Decide interaction/export policy later. |
| #81 Rotated occurrence-local AnchorFrame references | dev-cad | **later** | Investigate with #325. |
| #9 First-class Sketch/constraints/workplanes | dev-cad | **later** | Refresh epic and deliver focused slices. |
| #8 Hollow primitives | dev-cad | **later** | Reconcile with native shell/pipe/boolean histories. |
| #5 Generic anchors/parametric constraints | dev-cad | **probably obsolete** | Separate any remaining scope from #9. |

## Boundary

Forge may own:

- Forge-specific builder commands;
- model-specific SolidCraft verification definitions;
- visual/presentation policy;
- site content/rendering.

Forge must not own:

- generic PR diff/docs classification;
- CAD-CI planning/SCons/cache behavior;
- built-in build123d/CadQuery runtime batching;
- reusable mesh geometry verification;
- verification-package materialization/transport;
- durable build-store semantics;
- Pages placement/publication mechanics.

## Next release checkpoint

#740 is complete/closed. #721 synchronized `main -> dev-cad` at
`1a751317b8f1901118084ecc6e9f6faa9b1adf6b` and durable evidence is green.
Finish this #722 CAD-document restoration and require the restored dev-cad lane
green. Then complete #716 -> #714. Do not start #739 or merge another CAD/API
implementation batch before Forge v0.12.0 is published or explicitly deferred;
keeping `main` fixed avoids another history synchronization cycle.
