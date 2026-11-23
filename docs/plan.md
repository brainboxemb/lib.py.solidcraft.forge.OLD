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

#722 and #717 are complete and closed. The v0.12.0 source preparation is on
`main` at `72b50e49df74df4740ae9e46d2df59689dbd858d`, but publication is
blocked by two release-path fixes:

- #763: update the Forge-specific release check to the current CAD-CI Pages
  record;
- #739: replace Forge's local generic release code with the released
  `tool.py.lib.ci` reusable release workflow/template.

These two fixes belong on `dev-ci`. They do not block new Forge CAD/API work
on `dev-cad`; both tracks may proceed in parallel.

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

### WS1 — dev-ci: fix the release path and publish Forge v0.12.0

Status: **now, in parallel with WS2**.

Required order:

1. sync current `main` into `dev-ci`;
2. #763 updates only the Forge-owned release validator and its documentation/tests;
3. #739 replaces Forge's local command parsing/tag/GitHub Release code with the
   released `tool.py.lib.ci` release template and reusable workflow;
4. require the exact `dev-ci` head to pass its normal CI checks;
5. merge exact `dev-ci -> main` through the released merge policy;
6. require the resulting exact `main` commit to have a green main build,
   exact `forge-release` evidence and a stable Pages record for that source;
7. publish v0.12.0 only through the released reusable release workflow;
8. verify the annotated `v0.12.0` tag and GitHub Release.

The failed release run `45232338094` created no v0.12.0 tag or GitHub Release.
Do not publish through Forge's old local generic release implementation again.

### WS2 — dev-cad: continue Forge CAD/API work

Status: **now, in parallel with WS1**.

Start with #746, then continue the focused reusable Forge gaps in normal issue
order. Each issue stays on its own short-lived branch from current `dev-cad`
and merges back only after its focused tests are green.

Current order:

1. #746 — support Cone in boolean join/cut feature compilation;
2. #747 — Polygon2D explicit/attached Sketch compilation;
3. #748 — qualified STL export path;
4. #749 — isolate project-local modules between run_script roots;
5. #750 — standalone Shape local transform/rotation;
6. #751 — native SolidCraft exploded views;
7. #753 — component-local native Cylinder joins across copied/rotated occurrences.

The release-path work on `dev-ci` must not be copied into these CAD/API
branches. CAD/API changes on `dev-cad` must not be mixed into the release-path
fixes on `dev-ci`.

### WS3 — later repository/documentation work

- #713 scripts ownership audit — later, after the release path is on the shared
  release workflow;
- #737 historical changelog normalization — later / docs-only;
- #659 build/verification/results terminology — later;
- #570 CADCraft diagram replacement — later;
- #335 build123d Sheet Metal reference semantics — later.

Other longer-term API/research work remains later: #349, #347, #325, #81, #82,
#9 and #8. #175 and #5 remain probably obsolete in their current broad forms.

## Open issue assessment — 2026-11-23

| Issue | Owner/lane | Status | Next action |
| --- | --- | --- | --- |
| #739 Adopt tool.py.lib.ci release template | dev-ci | **now** | Remove Forge-local generic release handling and call the released reusable release workflow/template before v0.12.0 publication. |
| #763 Align release validation with CAD-CI Pages record | dev-ci | **now** | Update the Forge-specific validator to the current final Pages record and test it. |
| #714 Release Forge 0.12.0 | repository | **blocked on #763 + #739** | Publish only after both release-path fixes are merged through dev-ci to main and the new exact main build is green. |
| #746 Cone join/cut feature compilation | dev-cad | **now / WS2** | Reusable compiler gap; implement in the next CAD/API batch. |
| #747 Polygon2D explicit/attached Sketch compilation | dev-cad | **now / WS2** | Required by downstream CAD; no consumer workaround. |
| #748 Qualified STL export path | dev-cad/runtime owner | **now / WS2** | Determine native export owner, then qualify released path. |
| #749 Isolate project-local modules between run_script roots | dev-cad | **now / WS2** | Fix runner ownership, no consumer sys.modules workaround. |
| #750 Standalone Shape local transform/rotation | dev-cad | **now / WS2** | Add generic cutter transform support after release checkpoint. |
| #751 Native SolidCraft exploded views | dev-cad | **now / WS2** | Wrap/qualify native explode API after release checkpoint. |
| #753 Qualify component-local native Cylinder joins across copied/rotated occurrences | dev-cad | **now / WS2** | Draft PR #754 exists; retain it as the focused runtime/Forge qualification fixture and resume after the history/release checkpoint. |
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

The v0.12.0 source preparation is on `main` at
`72b50e49df74df4740ae9e46d2df59689dbd858d`. The next release publication
must first complete #763 and #739 on `dev-ci`, merge that exact branch back to
`main`, and pass the new exact main build.

At the same time, Forge CAD/API work continues independently on `dev-cad`,
starting with #746. Keep the two branch responsibilities separate.
