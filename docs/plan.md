# Forge repository plan

This file is the current source of truth for unfinished work in
`lib.py.solidcraft.forge`.

Forge owns the public CAD API/compiler/model behavior, Forge-specific
verification expectations and repository-specific release validation.
Generic CAD-CI, shared release mechanics, reusable verification, runtime
packaging, generated build branches, Pages and merge policy stay in their
owner repositories.

## Current repository state

Permanent source refs:

```text
main
dev-cad
dev-ci
```

Current heads at the v0.13.0 release checkpoint:

- `main`: `733134e66283e57c65a608731c04945fbf177b60`;
- `dev-cad`: `b83a53f60795ca8d08c452f132eab362974632e5`;
- `dev-ci`: `68905bdbd4d999d73248858b4c3f9336ad47cf6e`.

Published Forge package before this patch checkpoint: **v0.13.0** at exact
`fc44eb8c3ccbf5f945f69bf68d6076a0a4294f63`.

The annotated `v0.12.0` tag and GitHub Release are valid and immutable. That
release does not contain #746, #747, #749 or #750. The original `Cone`
primitive itself predates v0.12.0; #746 is specifically native Boolean feature
compilation for Cone.

## Permanent branch rule

- `main`: stable integration only.
- `dev-cad`: Forge API/compiler/model/verification/site-content work.
- `dev-ci`: CI/release integration.
- short-lived work branches are squash-merged;
- exact `main -> dev-cad|dev-ci`: history-preserving sync;
- exact `dev-cad|dev-ci -> main`: history-preserving sync;
- conflicted permanent-ref sync uses the released reviewed
  `/merge-resolved` path with a separate `resolve/` review branch;
- generic owner behavior is changed, released and externally accepted in its
  owner repository before Forge consumes it.

## Accepted shared stack

- `lib.py.cad.ci v0.18.2` @
  `088644a05ff698957aef2ddc6cc5de037ddfa158`;
- `tool.cad.ci v0.36.1` @
  `8a9acb8ea69581728a3850c658b4c1ae2db6ff5a`;
- `tool.py.lib.ci v0.2.1` @
  `58ead6897a4ac8cafef22a3c1f834491bf61568d`;
- `lib.py.cad.verification v0.16.0` @
  `c7c145b7be0c602724e8cca874ef29990baaad1e`;
- `docker.cad.solidcraft v0.3.4`.

The central release flow is proven by v0.12.0. Pages is web output and is not
release evidence. The stable release evidence is the main **ci-build-record**.

## Active work

### Release — #789 Forge v0.13.1

Status: **now**.

v0.13.0 is published and contains the intended post-v0.12 CAD batch. Its
release notes, however, did not explicitly explain that v0.12.0 had been cut
before #746/#747/#749/#750 reached stable main.

v0.13.1 is a documentation/release-metadata patch only:

1. package version becomes `0.13.1`;
2. changelog gets an explicit release-boundary explanation;
3. no modelling behavior changes from v0.13.0;
4. after merge, require the exact main branch build green;
5. publish with `/release v0.13.1 <exact-main-sha>`;
6. verify annotated tag and GitHub Release against that exact SHA;
7. update this plan to the published state.

Do not move or rewrite v0.12.0 or v0.13.0.

### CAD — #779 whole-sheet perforation

Status: **paused until the v0.13.0 release is complete**.

PR #780 is intentionally outside the frozen v0.13.0 batch. Its branch must be
refreshed from the current `dev-cad` after the release checkpoint. The feature
must become a Sheet metal Verification item before completion.

### Documentation / Verification — #785 and #786

Status: **issues recorded; implementation resumes after v0.13.0**.

- #785 restores the small curated public Examples catalog and introduces an
  independent Verification catalog with a first-class **Sheet metal** group.
- #786 makes Reference, API Guide, Cheatsheet and `docs/api.md` track new
  public Forge capabilities.
- new public modelling API is not considered documentation-complete without
  normal user-facing API documentation and Verification coverage.

### Shared CAD-CI terminology

`tool.cad.ci #180` tracks replacement of the public word `durable` with
clear branch-build terminology. Forge must wait for a released/accepted shared
change; do not add a local alias. The agreed release-evidence term
`ci-build-record` remains unchanged.

Exploded-view #751 remains deliberately lower priority.

## Completed CAD work awaiting v0.13.0 publication

- #746 Cone Boolean feature compilation;
- #747 Polygon2D explicit/attached Sketch;
- #749 model-local import isolation;
- #750 rotated standalone Sketch cutters;
- #773 native sheet hem;
- #776 native sheet path flange.

## Other open work

| Issue | Status | Next action |
| --- | --- | --- |
| #789 Release Forge v0.13.1 clarification patch | **now** | Merge metadata/docs patch, require exact main build, publish and verify v0.13.1. |
| #785 Examples / Verification catalog split | **after release** | Restore four curated Examples and add Sheet metal Verification group. |
| #786 API documentation completeness | **after release** | Add Sheet metal Reference/Guide/Cheatsheet/API coverage. |
| #779 Native whole-sheet perforation | **after release** | Refresh from dev-cad, finish runtime evidence and publish as Verification case. |
| #753 Component-local Cylinder joins | **later** | Refresh focused work after current checkpoint. |
| #751 Native exploded views | **lower priority** | Resume after higher-priority metal/docs work. |
| #737 Historical changelog alignment | **later / docs-only** | Keep separate from release behavior. |
| #713 Audit/reduce Forge scripts | **later** | Remove genuine duplicates after owner migrations settle. |
| #659 Build/verification/results terminology | **later / cross-repo** | Follow shared terminology work. |
| #570 Remove CADCraft from verification diagrams | **later** | Preserve presentation while replacing source format. |
| #349 Remaining SOLID CREATE coverage | **later** | Deliver focused reusable features when required. |
| #347 Generalized pattern seeds | **later** | Generalize through native feature identity. |
| #335 build123d Sheet Metal reference | **blocked upstream** | Wait for a released upstream Sheet Metal API. |
| #325 AnchorFrame root cause | **later** | Resume when an active model requires it. |
| #82 Joints-folder visibility | **later** | Decide interaction/export policy separately. |
| #81 Rotated occurrence-local AnchorFrame references | **later** | Investigate with #325. |
| #9 First-class Sketch/constraints/workplanes | **later / epic** | Continue through focused slices. |
| #8 Hollow primitives | **later** | Reconcile with native shell/pipe support when needed. |

## Next checkpoint

Finish #789 as Forge v0.13.1: merge the metadata/documentation patch to
`main`, require the exact resulting main branch build green, publish through
the central release flow, and verify the immutable tag/GitHub Release before
resuming #779, #785 or #786.
