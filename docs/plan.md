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

Current heads before the #781 synchronization completes:

- `main`: `c8677ac945f22495b04da7c2cef9dd06595c9cec`;
- `dev-ci`: `68905bdbd4d999d73248858b4c3f9336ad47cf6e`;
- `dev-cad`: `cc7ab64e02a277c1705bcfcd9f96cc6f16c53fab`.

Published Forge package: **v0.12.0** at exact
`68905bdbd4d999d73248858b4c3f9336ad47cf6e`.

The annotated `v0.12.0` tag and GitHub Release are valid and immutable.
However, that tag predates the later `dev-cad` model-unblocking batch. Do not
tell downstream users that v0.12.0 contains #746, #747, #749 or #750.

The original `Cone` primitive itself predates v0.12.0; the missing Cone change
is specifically #746 native Boolean feature compilation.

## Permanent branch rule

- `main`: stable integration only.
- `dev-cad`: Forge API/compiler/model/verification/site-content work.
- `dev-ci`: CI/release integration.
- short-lived work branches are squash-merged;
- exact `dev-cad|dev-ci -> main`: history-preserving normal merge;
- exact `main -> dev-cad|dev-ci`: history-preserving normal merge;
- conflicted permanent-ref sync/promotion uses the released reviewed
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

The central release flow is already proven by the successful v0.12.0
publication. Pages is web output and is not release evidence.

## Active work

### Release lane — #781 Forge v0.13.0

Status: **now, parallel with CAD work**.

Reason for v0.13.0:

- #746 Cone Boolean/native-feature support was merged after the v0.12.0 tag;
- #747 Polygon2D explicit/attached Sketch support was merged after the tag;
- #749 model-local import isolation was merged after the tag;
- #750 rotated standalone Sketch cutter support was merged after the tag;
- current dev-cad also contains new public sheet API (#773 and #776).

Required order:

1. **now** — resolve conflicted permanent sync PR #782 (`main -> dev-cad`)
   through the released reviewed `/merge-resolved` path;
2. require the resulting exact `dev-cad` durable run green;
3. promote exact `dev-cad -> main` history-preserving;
4. require the exact resulting main build green;
5. prepare v0.13.0 package metadata and dated changelog from that stable
   candidate on a dedicated #781 release-preparation branch/PR;
6. require the release-preparation main result green;
7. publish only through `/release v0.13.0 <exact-main-sha>`;
8. verify the annotated tag and GitHub Release resolve to that exact SHA;
9. reconcile this plan after publication.

Do not retag or move v0.12.0.

### CAD lane — #779 whole-sheet perforation

Status: **active in parallel; PR #780 exact-head green**.

#779 adds native whole-sheet `sheet.perforate` semantics without repeated
B-rep-hole approximation.

PR #780 at `9deca3a69d4ed599a756b58b8f59f748ce27c8ec` is green. Keep it open while
#782's reviewed conflict-resolution base is fixed; merging #780 first would move
`dev-cad` and invalidate the reviewed #782 base SHA. After #782 is complete,
refresh #780 against the synchronized lane if needed, then merge it normally
after exact-head green evidence.

Exploded-view #751 remains deliberately lower priority.

### Completed CAD work awaiting stable release

- #746 Cone Boolean feature compilation — dev-cad merge
  `611762e4f2eb1be02ec758f4a86cb519f1419fbc`;
- #747 Polygon2D explicit/attached Sketch — dev-cad merge
  `4625e57b39b344cb64ed4063cb7ea7c933fa7b15`;
- #749 model-local import isolation — dev-cad merge
  `fd836e4797a7672497fc63978902ff2306fd9b7a`;
- #750 rotated standalone Sketch cutters — dev-cad merge
  `84cb5b4b6b7085eb92865eafe28fd7478bb2665e`;
- #773 native sheet hem — dev-cad merge
  `c5586872244fa19db54818acef5e55b1bc36d95d`, durable run
  `45251444014` green;
- #776 native sheet path flange — dev-cad merge
  `cc7ab64e02a277c1705bcfcd9f96cc6f16c53fab`, durable run
  `45253180169` green.

## Open issue assessment — 2026-11-23

| Issue | Status | Next action |
| --- | --- | --- |
| #781 Release Forge v0.13.0 | **now / release** | Complete #782 sync, promote dev-cad, prepare and publish v0.13.0. |
| #779 Native whole-sheet perforation | **now / CAD parallel** | Keep green PR #780 open until #782 fixes the lane base, then refresh/merge. |
| #753 Component-local Cylinder joins | **next after current checkpoint** | Refresh focused work after release/perforation lane is stable. |
| #751 Native exploded views | **later / lower priority** | Resume after higher-priority metal/release work. |
| #750 Rotated standalone Shape cutters | **implemented, awaiting stable release** | Close after the post-v0.12 CAD batch is released. |
| #749 Model-local import isolation | **implemented, awaiting stable release** | Close after the post-v0.12 CAD batch is released. |
| #747 Polygon2D explicit/attached Sketch | **implemented, awaiting stable release** | Close after the post-v0.12 CAD batch is released. |
| #746 Cone Boolean feature compilation | **implemented, awaiting stable release** | Close after the post-v0.12 CAD batch is released. |
| #737 Historical changelog alignment | **later / docs-only** | Keep separate from release/CAD behavior. |
| #713 Audit/reduce Forge scripts | **later** | Remove only genuine duplicates after owner migrations settle. |
| #659 Build/verification/results terminology | **later / cross-repo** | Follow shared terminology work; do not mix into release. |
| #570 Remove CADCraft from verification diagrams | **later** | Preserve presentation behavior while replacing source format. |
| #349 Remaining SOLID CREATE coverage | **later** | Deliver focused reusable features when required. |
| #347 Generalized pattern seeds | **later** | Generalize through native feature identity. |
| #335 build123d Sheet Metal reference | **blocked upstream** | Wait for a released build123d Sheet Metal API; no unreleased pin or solid workaround. |
| #325 AnchorFrame root cause | **later** | Resume when an active model requires it. |
| #175 HUB75-like AnchorFrame diagnostic | **probably obsolete** | Move unique evidence into #325 if any remains. |
| #82 Joints-folder visibility | **later** | Decide interaction/export policy separately. |
| #81 Rotated occurrence-local AnchorFrame references | **later** | Investigate with #325. |
| #9 First-class Sketch/constraints/workplanes | **later / epic** | Continue through focused slices. |
| #8 Hollow primitives | **later** | Reconcile with native shell/pipe support when needed. |
| #5 Generic anchors/parametric constraints | **probably obsolete** | Split useful remaining scope into focused issues if needed. |

## Boundary

Forge may own:

- reusable CAD API/compiler behavior;
- `run_script()` model loading;
- Forge-specific builder commands;
- model-specific SolidCraft verification definitions;
- public Forge documentation;
- repository-specific release validation.

Forge must not own:

- generic CAD-CI planning/build-store behavior;
- generic build-record validation;
- generic tag/GitHub Release mechanics;
- Pages publication mechanics;
- reusable CAD verification internals;
- generic merge policy.

## Next checkpoint

Finish the reviewed #782 permanent-branch synchronization without moving its
base in parallel. Keep #780 green but unmerged until that synchronization
completes. Then resume both v0.13.0 promotion and #779 from the synchronized
`dev-cad` head.
