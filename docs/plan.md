# Forge repository plan

This file is the current source of truth for unfinished work in
`lib.py.solidcraft.forge`.

Forge owns the public CAD API/compiler/model behavior, Forge-specific release
rules and model-specific verification. Generic CAD-CI, release build checks,
tag/GitHub Release creation, Pages and merge policy stay in their owner
repositories.

## Current permanent branches

```text
main
dev-ci
dev-cad
```

Current heads:

- `main`: `68905bdbd4d999d73248858b4c3f9336ad47cf6e`;
- `dev-ci`: `68905bdbd4d999d73248858b4c3f9336ad47cf6e`;
- `dev-cad`: `84cb5b4b6b7085eb92865eafe28fd7478bb2665e`.

`main` and `dev-ci` are aligned after the released central-flow promotion.
`dev-cad` remains the independent CAD/API lane.

## Accepted shared CI/release stack

- `lib.py.cad.ci v0.18.2` @
  `088644a05ff698957aef2ddc6cc5de037ddfa158`;
- `tool.cad.ci v0.36.1` @
  `8a9acb8ea69581728a3850c658b4c1ae2db6ff5a`;
- `tool.py.lib.ci v0.2.1` @
  `58ead6897a4ac8cafef22a3c1f834491bf61568d`;
- `lib.py.cad.verification v0.16.0` @
  `c7c145b7be0c602724e8cca874ef29990baaad1e`;
- `docker.cad.solidcraft v0.3.4`.

The central CAD release flow is externally accepted in
`tool.cad.ci.test #256`.

Acceptance proved on exact test-consumer main commit
`9558d1a2e49ddcc252b6e646f4a16c66e52d3ffa`:

- stale release source refused by the stable main `ci-build-record`;
- exact main source released successfully;
- repeated exact command succeeded without creating a second release;
- the annotated tag resolved to the exact source commit;
- Pages was not used as release evidence.

## Active work

### dev-ci — central release flow

Status: **complete and released on stable main**.

- #739 / PR #772 adopted the released `tool.cad.ci v0.36.1` wrapper on
  `dev-ci`;
- PR #774 promoted exact `dev-ci -> main` through the shared history-preserving
  merge policy at `68905bdbd4d999d73248858b4c3f9336ad47cf6e`;
- main durable run `45250190637` succeeded and published exact build evidence;
- #714 published Forge **v0.12.0** through the central flow;
- annotated tag `v0.12.0` resolves to exact
  `68905bdbd4d999d73248858b4c3f9336ad47cf6e`;
- GitHub Release `v0.12.0` is published and release run `45250563106`
  completed successfully.

Issue #763 remains closed as **not planned**: generic build/Page release checks
belong to the shared owner layer.

### dev-cad — Forge CAD/API work

Work completed on `dev-cad`:

- #746 Cone boolean join/cut — merge `611762e4...`;
- #747 Polygon2D explicit/attached Sketch — merge `4625e57b...`;
- #748 STL export — closed; native SolidCraft CLI export is consumer/build
  adapter responsibility;
- #749 model-local Python import isolation — merge `fd836e47...`;
- #750 rotated standalone Sketch cutters — merge
  `84cb5b4b6b7085eb92865eafe28fd7478bb2665e`.

The exact #750 dev-cad build run `45246647800` is green.

Current order:

1. **now — metal** — #773 native `sheet.hem` on existing sheet bodies;
2. **next metal candidate** — #776 native `sheet.path_flange`, reusing the
   existing-sheet history and #683 open-chain contract;
3. #753 component-local native Cylinder joins across copied/rotated
   occurrences;
4. #751 native SolidCraft exploded views — deliberately lower priority.

#335 build123d Sheet Metal reference is upstream-blocked until a released
build123d version contains the newer Sheet Metal API. Do not replace the
reference with another solid approximation or pin an unreleased upstream
revision.

Keep CAD/API changes on `dev-cad`; do not mix release-flow changes into these
branches.

## Open issue assessment — 2026-11-23

| Issue | Branch/owner | Status | Next |
| --- | --- | --- | --- |
| #739 central CAD release flow | dev-ci/main | **complete** | Released central wrapper is on stable main via PR #774. |
| #714 Release Forge 0.12.0 | main/release | **complete** | v0.12.0 is published at exact `68905bdbd4d999d73248858b4c3f9336ad47cf6e`; reconcile docs/plan and close. |
| #746 Cone boolean compilation | dev-cad | **implemented on dev-cad** | Close/promote with the current CAD batch. |
| #747 Polygon2D explicit/attached Sketch | dev-cad | **implemented on dev-cad** | Close/promote with the current CAD batch. |
| #749 model-local Python imports | dev-cad | **implemented on dev-cad** | Close/promote with the current CAD batch. |
| #750 rotated standalone Sketch cutters | dev-cad | **implemented on dev-cad** | Downstream CornerBracket may consume after a Forge release containing it. |
| #773 Native sheet.hem | dev-cad | **now / metal** | Finish exact-head SolidCraft qualification and merge through the shared policy. |
| #776 Native sheet.path_flange | dev-cad | **after #773 / metal** | Reuse existing-sheet history and the #683 open-chain contract. |
| #753 component-local Cylinder joins | dev-cad | **after metal slice** | Refresh focused draft after the current metal work. |
| #751 native exploded views | dev-cad | **later / lower priority** | Resume after the higher-priority metal/runtime work. |
| #713 audit/reduce Forge scripts | repository | later | Reassess after #739 removes local release plumbing. |
| #737 historical changelog alignment | docs | later / docs-only | Keep separate. |
| #659 build/verification/results terminology | cross-repo | later | Follow shared plain-language work. |
| #570 CADCraft diagram replacement | dev-cad | later | Preserve presentation behavior while replacing source format. |
| #349 remaining SOLID CREATE coverage | dev-cad | later | Focused slices only. |
| #347 generalized pattern seeds | dev-cad | later | Generalize by native feature identity. |
| #335 build123d Sheet Metal reference | dev-cad/upstream | **blocked** | Wait for a released build123d Sheet Metal API; no unreleased pin or replacement approximation. |
| #325 AnchorFrame root cause | dev-cad | later | Resume with an active consumer need. |
| #175 HUB75 AnchorFrame diagnostic | dev-cad | probably obsolete | Move unique evidence to #325. |
| #82 Joints-folder visibility | dev-cad | later | Decide later. |
| #81 rotated occurrence-local AnchorFrame | dev-cad | later | Investigate with #325. |
| #9 Sketch/constraints/workplanes epic | dev-cad | later | Deliver focused issues separately. |
| #8 hollow primitives | dev-cad | later | Reconcile with native shell/pipe/boolean support. |
| #5 generic anchors/constraints | dev-cad | probably obsolete | Separate any remaining scope from #9. |

## Boundary

Forge may own:

- CAD API/compiler/model behavior;
- Forge-specific version/changelog/blocker release checks;
- model-specific SolidCraft verification;
- presentation/site content.

Forge must not own:

- generic CAD-CI build checks;
- parsing `main/build.json` for release qualification;
- Pages as release evidence;
- generic `/release` parsing;
- tag/GitHub Release creation or idempotency;
- generic release reporting;
- merge-policy mechanics.

## Next checkpoint

Forge v0.12.0 and the central release-flow migration are complete on stable
`main`. Continue #773 on `dev-cad`, then #776 as the next metal candidate.
Keep #751 exploded views at lower priority.
