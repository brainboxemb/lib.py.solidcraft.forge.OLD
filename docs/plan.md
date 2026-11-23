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

Current permanent heads after #716 promotion:

- `main`: `5e63112a82f0d30f0006c0e7de3fed7f8f69ebf5`;
- `dev-cad`: `5e63112a82f0d30f0006c0e7de3fed7f8f69ebf5`;
- `dev-ci`: `90ac473473ab954103190ba426b350852b380fc0`.

#716 promoted the reconciled post-v0.11 CAD batch through the released
permanent-lane merge policy. Exact-head PR run `45228705759`, main durable run
`45229452632` and dev-cad durable run `45229458378` are green. Stable
`build/main`, Pages and Verification provenance all identify exact
`5e63112...`.

#722 and #717 are complete and closed. The active gate is now #714:
prepare one explicit v0.12.0 release candidate, then require all release
evidence on the exact preparation commit before publication.

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

### WS1 — prepare and publish Forge v0.12.0

Status: **now**. The CAD-CI cut-over, dev-cad history reconciliation and #716
promotion are complete.

Required order:

1. **complete** — #716 promoted exact `dev-cad -> main` at
   `5e63112a82f0d30f0006c0e7de3fed7f8f69ebf5`;
2. **complete** — exact promoted main/dev-cad durable integration and stable
   Pages/Verification provenance are green;
3. **now** — #714 creates the explicit release-preparation commit: v0.12.0
   changelog inventory, package version `0.12.0`, and exact candidate plan;
4. require the resulting exact main SHA to have green `build/main`,
   `forge-release`, `release-policy` and stable Pages evidence;
5. publish only with `/release v0.12.0 <exact-main-sha>`, then independently
   verify the annotated tag and GitHub Release.

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
| #714 Release Forge 0.12.0 | repository | **now** | Promotion gate is green; prepare exact v0.12.0 candidate, qualify that exact main SHA, then publish through `/release`. |
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

The post-v0.11 CAD/CI batch is on stable `main` at
`5e63112a82f0d30f0006c0e7de3fed7f8f69ebf5` with exact durable/Page
provenance green. #714 is now the only release checkpoint: merge the v0.12.0
preparation, qualify that exact resulting main SHA, publish the immutable
`v0.12.0` tag/GitHub Release, and reconcile the plan afterward.

Do not start #739 or merge another CAD/API implementation batch before the
release is published or explicitly deferred.
