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

Current permanent heads at this checkpoint:

- `main`: `80bc83e72e34e0dce6e6df745d2ebf8f96111379`;
- `dev-cad`: `e4ea4bcaf8fba1e3fd9d18dac84aaadaf7d261d3`;
- `dev-ci`: `8c24f884b18eb17b25cce3b3c3237dee67de71eb`.

Forge #785 / PR #816 is accepted on `dev-cad`. Exact durable branch run
`45358578565` succeeded and published the accepted dev-cad build/Page state.
The earlier accidental #811 directory split is fully reverted and is not part
of the active architecture.

Latest published Forge package: **v0.13.2** at exact
`ea5710a5d2d33b0633b93c5da95dd5b74f126aa4`.

The exact v0.13.2 main branch build `45269510406` and central release run
`45269991837` succeeded. No Forge release is currently active.

## Permanent branch rule

- `main`: stable integration only.
- `dev-cad`: Forge API/compiler/model/Verification/site-content work.
- `dev-ci`: CI/release integration.
- short-lived work branches are squash-merged;
- exact `main -> dev-cad|dev-ci`: history-preserving sync;
- exact `dev-cad|dev-ci -> main`: history-preserving promotion;
- conflicted permanent-ref sync uses the released reviewed
  `/merge-resolved` path;
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

Pages is web output and is not release evidence. Stable release evidence is the
main **ci-build-record**.

## Active execution

### #817 — reconcile plan after #785

Status: **now / docs-only dev-cad**.

This issue records the accepted #785 dev-cad state and restores complete open
issue assessment before stable promotion. It contains no implementation change.

### #785 — canonical model purpose and public catalogs

Status: **complete on dev-cad; stable promotion pending**.

Accepted contract:

```yaml
purpose: example
purpose: verification
purpose: [example, verification]
```

The source corpus remains under its existing model directories. There is no
semantic `examples/` versus `verification/cases/` split, no `catalog.yml`,
and `role.yml` is not public catalog membership.

The four curated teaching models carry both Example and Verification purposes.
The public Examples and Verification views select independently from normalized
`model.yml.purpose`. Sheet metal is a first-class Verification group.
Independent references and visual regression evidence are declaration-driven;
native integration/model/geometry verification remains mandatory.

Next action: promote accepted `dev-cad` through `main`. Close #785 after the
stable promotion is accepted.

### #779 — native whole-sheet perforation

Status: **now / dev-cad**.

PR #780 is based on the pre-#785 catalog contract and is 24 commits behind the
accepted dev-cad line. Rebuild that existing issue branch from current
`dev-cad` rather than copying stale plan/catalog files.

Keep the focused native `Shape.perforate()` API/compiler/runtime work, but:

- replace the old regression-only `role.yml` with canonical
  `model.yml` using `purpose: verification` and `section: sheet-metal`;
- keep the case at `examples/sheet-perforate/`;
- add normal user-facing API documentation required by #786: Reference,
  Sheet metal Guide, Cheatsheet and `docs/api.md`;
- preserve native perforation/flat-pattern semantics and do not fabricate
  repeated B-rep holes or external reference equivalents.

### #814 — Example basic validation selection

Status: **now / dev-ci**.

The existing first/basic Forge validation stage is already
`forge-release` / `scripts/tool_verify.py`. It currently duplicates the four
teaching slugs in `PASSING_EXAMPLES`.

Stable #785 is now synchronized to `dev-ci` by PR #815 / merge
`8c24f884b18eb17b25cce3b3c3237dee67de71eb`. #814 replaces the duplicate
passing-slug list with canonical `model.yml` selection whose normalized purpose
contains `example`. The separate `custom-anchor` expected-rejection policy
fixture remains explicit.

CAD-CI changed-path watches stay static and conservative: the release item watches
all model metadata/source/test paths, while `tool_verify.py` performs the
canonical purpose selection. This avoids a second slug registry without adding a
Forge-local scheduler.

### #788 — CAD-CI concurrency measurement

Status: **parallel / performance**.

Measure jobs=2/4/6 on one identical post-#785 representative full graph before
changing Forge concurrency or designing bounded batch sharding. Do not remove
Verification coverage or reintroduce per-model runtime startup.

## Open issue assessment

| Issue | Status | Next action |
| --- | --- | --- |
| #817 Plan reconciliation after #785 | **now / docs-only** | Merge the current snapshot to dev-cad before stable promotion. |
| #814 Example basic validation selection | **now / dev-ci** | Derive forge-release passing models from canonical `purpose: example`; keep static watches generic rather than duplicating slugs. |
| #788 Re-benchmark Forge CAD-CI concurrency | **parallel / performance** | Measure jobs=2/4/6 on one identical post-#785 full graph. |
| #785 Examples / Verification purpose split | **complete on dev-cad / promotion pending** | Promote accepted dev-cad to main; then close. |
| #779 Native whole-sheet perforation | **now / CAD** | Rebuild PR #780 on post-#785 dev-cad, publish as Sheet metal Verification and complete API docs. |
| #753 Component-local Cylinder joins | **later** | Refresh focused qualification after the active metal slice. |
| #751 Native exploded views | **lower priority** | Resume after higher-priority metal/runtime work. |
| #737 Historical changelog alignment | **later / docs-only** | Keep separate from release behavior. |
| #713 Audit/reduce Forge scripts | **later** | Remove genuine duplicates only after owner migrations settle. |
| #659 Build/verification/results terminology | **later / cross-repo** | Follow the released shared terminology work; do not add Forge-local aliases. |
| #570 Remove CADCraft from verification diagrams | **later** | Preserve presentation while replacing the source format. |
| #349 Remaining SOLID CREATE coverage | **later** | Deliver focused reusable features when required. |
| #347 Generalized pattern seeds | **later** | Generalize through native feature identity. |
| #335 build123d Sheet Metal reference | **blocked upstream** | Wait for a released upstream Sheet Metal API. |
| #325 AnchorFrame root cause | **later / research** | Resume when an active product model requires the unresolved root-cause work. |
| #175 HUB75-like AnchorFrame diagnostic change | **later / diagnostic with #325** | Preserve the retained A/B evidence; resume its symbolic attached-seed/native comparison only as part of the #325 root-cause track. |
| #82 Joints-folder visibility | **later** | Decide interaction/export policy separately. |
| #81 Rotated occurrence-local AnchorFrame references | **later** | Investigate together with #325 when needed. |
| #9 First-class Sketch/constraints/workplanes | **later / epic** | Continue through focused qualified slices rather than one monolithic implementation. |
| #8 Hollow primitives | **later** | Reconcile with native shell/pipe support when a concrete model requires it. |
| #5 Generic anchors and parametric constraints | **later / foundational epic** | Treat as historical umbrella; continue only through focused issues with current native contracts. |

## Next checkpoint

1. merge #817 docs-only plan reconciliation to `dev-cad`;
2. in parallel:
   - open the normal `dev-cad -> main` promotion for accepted #785;
   - rebuild #779 / PR #780 on the post-#785 dev-cad line;
   - keep #788 measurement work independent;
3. after the stable promotion is green and merged:
   - close #785;
   - sync `main -> dev-ci`;
   - implement #814 against the accepted purpose-aware metadata contract;
4. keep #753 and #751 behind the active metal/runtime work.
