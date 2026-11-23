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

Current heads after v0.13.1 publication:

- `main`: `17a4e1d0e2edf0124d40daf5425891fdf65c24be`;
- `dev-cad`: `ee7f8ef6ff4e9942310d82f50f8be6b93714ef51`;
- `dev-ci`: `68905bdbd4d999d73248858b4c3f9336ad47cf6e`.

Latest published Forge package: **v0.13.1** at exact
`17a4e1d0e2edf0124d40daf5425891fdf65c24be`.

Central release run `45262594629` succeeded; the annotated `v0.13.1` tag and
GitHub Release both resolve to that exact commit.

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

### CAD regression — #796 symbolic placed-Cylinder anchors

Status: **now / release-blocking for the product-CAD consumer**.

CAD adoption PR #406 proved that released Forge v0.13.1 regresses a valid
parametric placed Cylinder used by `hub75-panel`. Run `45263158238` fails
in `_dim_add()` because the placed3d path converts a symbolic coordinate to a
native string expression before Cylinder anchor arithmetic combines it with an
Expression height.

Fix the generic conversion boundary in Forge, add focused Cylinder coverage and
cover the shared placed Cone path where applicable. Do not require the consumer
to bake parameter values or add a model-local workaround. After exact-head
qualification, #800 publishes the v0.13.2 patch release before CAD #405 can proceed.

### Release — v0.13.1

Status: **complete**.

- v0.13.0 published the intended post-v0.12 CAD batch;
- #789 added the missing release-boundary explanation as patch release v0.13.1;
- exact main branch build `45262080873` passed at
  `17a4e1d0e2edf0124d40daf5425891fdf65c24be`;
- central release run `45262594629` published and verified v0.13.1;
- v0.12.0, v0.13.0 and v0.13.1 remain immutable.

No active Forge release work remains.

### CAD — #779 whole-sheet perforation

Status: **resume now**.

PR #780 was intentionally kept outside the v0.13.x release batch. Refresh its
branch from current `dev-cad`, finish the native perforation evidence, and make
the feature a Sheet metal Verification item before completion.

### Documentation / Verification — #785 and #786

Status: **resume now in parallel with #779**.

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

## CAD work released in v0.13.0+

- #746 Cone Boolean feature compilation;
- #747 Polygon2D explicit/attached Sketch;
- #749 model-local import isolation;
- #750 rotated standalone Sketch cutters;
- #773 native sheet hem;
- #776 native sheet path flange.

## Other open work

| Issue | Status | Next action |
| --- | --- | --- |
| #796 Symbolic placed-Cylinder anchor arithmetic | **now / CAD regression** | Preserve Parameter/Expression values through anchor arithmetic and qualify Cylinder/shared primitive paths. |
| #800 Forge v0.13.2 hotfix release | **next / release** | After #796 reaches stable main with a green exact build, publish the smallest patch release for CAD #405/#406. |
| #789 Release Forge v0.13.1 clarification patch | **complete** | Published and verified at exact `17a4e1d0e2edf0124d40daf5425891fdf65c24be`. |
| #779 Native whole-sheet perforation | **now / CAD** | Refresh from dev-cad, finish runtime evidence and publish as a Sheet metal Verification case. |
| #785 Examples / Verification catalog split | **now / docs+verification** | Restore four curated Examples and add a Sheet metal Verification group. |
| #786 API documentation completeness | **now / docs** | Add Sheet metal Reference/Guide/Cheatsheet/API coverage. |
| #788 Re-benchmark Forge CAD-CI concurrency | **parallel / performance** | Measure jobs=2/4/6 on the same graph before changing batching. |
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

1. fix and qualify #796 first because it blocks adoption of the released
   capability batch in the product-CAD repository;
2. complete #800 and publish v0.13.2 containing #796 so CAD #405
   can qualify a corrected exact Forge release;
3. resume #779, #785 and #786 from the post-release refs in parallel where they
   do not depend on #796;
4. keep #788 as a separate measured performance lane and #751 exploded views at
   lower priority.
