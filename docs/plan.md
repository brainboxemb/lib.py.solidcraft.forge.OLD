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

- `main`: `74e44e98bb561992547609b24b2e2664356423a1`;
- `dev-ci`: `8d8bf2ad7e229500a75f8c1e3043cb8245de01d6`;
- `dev-cad`: `84cb5b4b6b7085eb92865eafe28fd7478bb2665e`.

`main` is already an ancestor of `dev-ci`; no additional `main -> dev-ci`
sync is required before #739.

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

### dev-ci — #739 central release flow

Status: **now**.

Forge is now allowed to consume the released central flow.

Required order:

1. replace `.github/workflows/release.yml` with the copy-ready
   `tool.cad.ci v0.36.1` CAD release wrapper;
2. pass `validator_path: scripts/release/validate_release.py`;
3. reduce the Forge validator to Forge-owned rules only:
   - release blocker file;
   - package version;
   - dated CHANGELOG release section / release notes;
   - tested SolidCraft version;
4. remove local CAD build-record and Pages release checks;
5. remove the local generic release publisher and its tests;
6. update `release-policy` to test only the Forge validator and wrapper
   contract;
7. require the #739 PR and resulting `dev-ci` build green;
8. merge exact `dev-ci -> main`;
9. require the new exact main build green;
10. publish Forge v0.12.0 through the central CAD release flow and verify the
    annotated tag/GitHub Release.

Issue #763 is closed as **not planned**: Forge does not adapt its old local
build/Page release checks.

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

1. **now** — #751 native SolidCraft exploded views;
2. #753 component-local native Cylinder joins across copied/rotated
   occurrences.

Keep CAD/API changes on `dev-cad`; do not mix release-flow changes into these
branches.

## Open issue assessment — 2026-11-23

| Issue | Branch/owner | Status | Next |
| --- | --- | --- | --- |
| #739 central CAD release flow | dev-ci | **now** | Consume exact released v0.36.1 wrapper, remove local publisher/build/Page checks. |
| #714 Release Forge 0.12.0 | main/release | **blocked on #739** | Publish after #739 reaches main and the exact main build is green. |
| #746 Cone boolean compilation | dev-cad | **implemented on dev-cad** | Close/promote with the current CAD batch. |
| #747 Polygon2D explicit/attached Sketch | dev-cad | **implemented on dev-cad** | Close/promote with the current CAD batch. |
| #749 model-local Python imports | dev-cad | **implemented on dev-cad** | Close/promote with the current CAD batch. |
| #750 rotated standalone Sketch cutters | dev-cad | **implemented on dev-cad** | Downstream CornerBracket may consume after a Forge release containing it. |
| #751 native exploded views | dev-cad | **now** | Wrap native explode.create/show behavior and qualify real SolidCraft replay. |
| #753 component-local Cylinder joins | dev-cad | **next** | Refresh focused draft after #751. |
| #713 audit/reduce Forge scripts | repository | later | Reassess after #739 removes local release plumbing. |
| #737 historical changelog alignment | docs | later / docs-only | Keep separate. |
| #659 build/verification/results terminology | cross-repo | later | Follow shared plain-language work. |
| #570 CADCraft diagram replacement | dev-cad | later | Preserve presentation behavior while replacing source format. |
| #349 remaining SOLID CREATE coverage | dev-cad | later | Focused slices only. |
| #347 generalized pattern seeds | dev-cad | later | Generalize by native feature identity. |
| #335 build123d Sheet Metal reference | dev-cad | later | Replace approximation when needed. |
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

Finish #739 on `dev-ci` and #751 on `dev-cad` independently.

After #739 reaches stable `main` and the exact main build is green, publish
Forge v0.12.0 through the central CAD release flow.
