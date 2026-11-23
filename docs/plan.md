# Forge repository plan

This file is the current source of truth for unfinished work in
`lib.py.solidcraft.forge`.

Forge owns the public CAD API/compiler/model behavior, Forge-specific
verification expectations and repository-specific release validation.
Generic CAD-CI, shared release mechanics, reusable verification, runtime
packaging, generated build branches, Pages and merge policy stay in their
owner repositories.

## Current release

Latest published Forge release: **v0.13.1**.

- annotated tag: `v0.13.1`;
- exact release source:
  `17a4e1d0e2edf0124d40daf5425891fdf65c24be`;
- central release run: `45262594629`;
- qualified SolidCraft: `0.45.0`.

v0.13.1 adds no modelling behavior beyond v0.13.0. It corrects release
guidance around the v0.12.0 -> v0.13.x boundary.

v0.12.0 and v0.13.0 remain valid immutable releases. The important boundary is
that #746, #747, #749 and #750 were not present in v0.12.0 and first reached a
published release in v0.13.0.

## Permanent branches

```text
main
dev-cad
dev-ci
```

At v0.13.1 publication:

- `main` release source:
  `17a4e1d0e2edf0124d40daf5425891fdf65c24be`;
- `dev-cad`:
  `733134e66283e57c65a608731c04945fbf177b60`;
- `dev-ci`:
  `68905bdbd4d999d73248858b4c3f9336ad47cf6e`.

Branch rules:

- `main`: stable integration only;
- `dev-cad`: Forge API/compiler/model/verification/site-content work;
- `dev-ci`: CI/release integration;
- short-lived work branches are squash-merged;
- exact `main -> dev-cad|dev-ci`: history-preserving sync;
- exact `dev-cad|dev-ci -> main`: history-preserving sync;
- conflicted permanent-ref sync uses the released reviewed
  `/merge-resolved` path with a separate `resolve/` review branch;
- generic owner behavior is changed, released and externally accepted in its
  owner repository before Forge consumes it.

Do not use vague process names such as “promotion” or “reconciliation” where a
concrete sync direction or build action is meant.

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

Pages is web output and is not release evidence. The stable release evidence is
the main **ci-build-record**.

## Active work

### #779 — native whole-sheet perforation

Status: **resume after v0.13.1**.

PR #780 is outside the v0.13.x release batch and must be refreshed from current
`dev-cad` before completion.

Required next steps:

1. refresh the branch from current `dev-cad`;
2. finish native SolidCraft flat-pattern/perforation evidence;
3. make perforation a visible **Sheet metal** Verification item;
4. require exact-head green evidence;
5. merge normally to `dev-cad`.

Do not model perforations as repeated B-rep holes.

### #785 — Examples / Verification catalog split

Status: **active next**.

Restore the architectural boundary:

- public Examples stays a small curated teaching catalog;
- Verification becomes an independent growing capability catalog;
- add a first-class **Sheet metal** Verification group;
- new public feature cases belong under `verification/cases/`;
- adding Verification coverage must not increase the public Example count.

Curated public Examples:

- `simple-box`;
- `anchored-holes`;
- `components`;
- `corner-anchor`.

The Sheet metal Verification group must include the existing sheet API family,
including base/fold, edge flange, contour flange, hem and path flange, with
perforation added when #779 is complete.

### #786 — API documentation completeness

Status: **active next, parallel with #785**.

Make normal user-facing API documentation track new public Forge capabilities.

Required surfaces:

- implementation docstrings;
- generated API Reference;
- task-oriented API Guide;
- Cheatsheet where appropriate;
- `docs/api.md` for cross-object semantics;
- Verification links/cases for behavior evidence.

Sheet metal must become a first-class API documentation domain rather than a few
isolated methods hidden in generic sections.

### #788 — Forge CAD-CI performance

Status: **measure before redesign**.

Current full Forge graphs are again around 2m17–2m49 for the CAD graph.

Important measured facts:

- Forge currently runs with `jobs=2`;
- the SolidCraft model batch has grown from 15 to about 45 cases;
- `model-verification-batch:verify_models` alone takes about 53 seconds;
- one of two parallel slots is therefore occupied by one large serial batch.

First perform controlled jobs=2/4/6 measurements on the same graph. Only design
bounded batch sharding if the model batch remains the critical path.

### Shared CAD-CI follow-ups

Owner issues:

- `tool.cad.ci #180`: replace public `durable` terminology with clear
  branch-build terminology;
- `lib.py.cad.ci #139`: keep parallel command output attributable to its CAD
  target while retaining live streaming and parallelism.

Forge must consume released shared changes; do not add local aliases/workarounds.

### Lower-priority Forge work

- #753 component-local Cylinder joins;
- #751 native exploded views;
- #737 historical changelog alignment;
- #713 audit/reduce Forge scripts;
- #659 build/verification/results terminology;
- #570 verification diagram source cleanup;
- #349 remaining SOLID CREATE coverage;
- #347 generalized pattern seeds;
- #335 build123d Sheet Metal reference — blocked on a released upstream API;
- #325 AnchorFrame root cause;
- #82 Joints-folder visibility;
- #81 rotated occurrence-local AnchorFrame references;
- #9 first-class Sketch/constraints/workplanes;
- #8 hollow primitives.

## Completed release batch

Released by v0.13.0/v0.13.1:

- #746 Cone Boolean feature compilation;
- #747 Polygon2D explicit/attached Sketch;
- #749 model-local import isolation;
- #750 rotated standalone Sketch cutters;
- #773 native sheet hem;
- #776 native sheet path flange.

## Next checkpoint

Resume #779, #785 and #786 from the post-v0.13.1 state. Keep exploded-view #751
at lower priority. Measure #788 separately without weakening Verification
coverage.
