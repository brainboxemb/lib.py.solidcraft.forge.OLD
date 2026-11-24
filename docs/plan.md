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

Current heads at the #785 restart checkpoint:

- `main`: `42f27142888d19fd87d84db9365bf3aed0cc73f2`;
- `dev-cad`: `704f344e93496e02c28d587faa57885f9be68eaf`;
- `dev-ci`: `68905bdbd4d999d73248858b4c3f9336ad47cf6e` (main -> dev-ci sync PR #815 in progress).

PR #811's directory/catalog split was accidentally merged and then exactly
reverted by #812/#813. The restored dev-cad tree is byte-for-byte equivalent
to the pre-#811 tree; #785 now restarts from the corrected architecture.

Latest published Forge package: **v0.13.2** at exact
`ea5710a5d2d33b0633b93c5da95dd5b74f126aa4`.

Exact main branch build `45269510406` and central release run
`45269991837` succeeded; the annotated `v0.13.2` tag and GitHub Release both
resolve to that exact commit.

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

Status: **complete; released in v0.13.2**.

The generic Forge fix is merged and qualified:

- `dev-cad`: `926feda24ee61c01ab5bfe00521b6aae0c4ede2a`;
- dev-cad branch build: `45267112890` green;
- stable `main`: `9df3a2fa5634ea1d44046959a54b4a8f060ab603`;
- main branch build: `45268325135` green.

The fix keeps placed primitive coordinates typed through anchor arithmetic and
covers the HUB75-style Cylinder path plus shared Box/Cone lowering. No
product-CAD workaround was added.

### Release — v0.13.2

Status: **complete**.

- exact release source:
  `ea5710a5d2d33b0633b93c5da95dd5b74f126aa4`;
- exact main branch build: `45269510406` green;
- central release run: `45269991837` green;
- annotated `v0.13.2` tag resolves exactly to the release source;
- GitHub Release `v0.13.2` is published and verified;
- v0.13.2 is the corrected consumer target for the #796 regression.

No active Forge release work remains.

### Release — v0.13.1

Status: **complete**.

- v0.13.0 published the intended post-v0.12 CAD batch;
- #789 added the missing release-boundary explanation as patch release v0.13.1;
- exact main branch build `45262080873` passed at
  `17a4e1d0e2edf0124d40daf5425891fdf65c24be`;
- central release run `45262594629` published and verified v0.13.1;
- v0.12.0, v0.13.0 and v0.13.1 remain immutable.

v0.13.1 and v0.13.2 are complete and immutable. No Forge release is currently active.

### CAD — #779 whole-sheet perforation

Status: **next after #785**.

PR #780 was intentionally kept outside the v0.13.x release batch. Refresh it
from the accepted #785 dev-cad head, keep its source under the existing
`examples/sheet-perforate` layout, finish native perforation evidence and set
its canonical model metadata purpose to include `verification`.

### Documentation / Verification — #785 and #786

Status: **#785 now on dev-cad; #786 complete**.

#785 uses the canonical shared `model.yml` contract rather than source
directory semantics:

- add `purpose` with accepted values `example`, `verification`, or a YAML
  list containing both;
- keep all model source paths in their existing `examples/<slug>` locations;
- select the curated Examples catalog from purpose containing `example`;
- select the broader Verification catalog from purpose containing
  `verification`;
- keep the four curated examples as `[example, verification]`;
- promote the recent sheet-metal, attached Polygon2D and rotated Sketch
  capabilities to Verification in-place;
- make external reference implementations optional evidence when the source
  implementation is absent;
- add the first-class **Sheet metal** Verification group;
- do not use `role.yml`, `catalog.yml` or directory placement as the public
  catalog contract.

#786 is complete: Sheet metal is already first-class in Guide, Reference,
Cheatsheet and `docs/api.md`.

#814 is the separate dev-ci consumer of `purpose: example`: it will derive
Forge's small first/basic model validation set from the same canonical metadata
instead of maintaining a second hardcoded slug list. Its implementation waits
for the accepted #785 metadata contract to reach dev-ci.

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
| #796 Symbolic placed-Cylinder anchor arithmetic | **complete / v0.13.2** | Released and verified; downstream CAD should consume v0.13.2 without a model workaround. |
| #800 Forge v0.13.2 hotfix release | **complete** | Published and verified at exact `ea5710a5d2d33b0633b93c5da95dd5b74f126aa4`. |
| #789 Release Forge v0.13.1 clarification patch | **complete** | Published and verified at exact `17a4e1d0e2edf0124d40daf5425891fdf65c24be`. |
| #779 Native whole-sheet perforation | **next after #785** | Refresh from accepted #785 dev-cad, keep existing source path, add verification purpose and finish runtime evidence. |
| #785 Purpose-based Examples / Verification catalogs | **now / dev-cad** | Add canonical model.yml purpose, restore four curated Examples, promote recent Verification cases in place and add Sheet metal grouping. |
| #786 API documentation completeness | **complete** | Sheet metal is first-class in Reference, Guide, Cheatsheet and cross-object API documentation. |
| #812 Revert accidental #811 catalog split | **complete / recovery** | PR #813 restored the exact pre-#811 tree without history rewrite. |
| #814 Purpose-driven basic Forge validation set | **blocked on #785 contract / dev-ci** | After #785 reaches dev-ci, derive the small first/basic validation set from purpose containing example. |
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

1. finish #785 on the restored dev-cad tree and require its exact branch build
   green;
2. complete main -> dev-ci sync PR #815 independently;
3. after #785 is accepted and synchronized to dev-ci, implement #814 so the
   first/basic Forge model set comes from `model.yml.purpose`;
4. refresh #779 from the accepted #785 dev-cad head and add perforation as
   another in-place Sheet metal Verification model;
5. keep #788 as a separate measured performance lane and #751 exploded views at
   lower priority.
