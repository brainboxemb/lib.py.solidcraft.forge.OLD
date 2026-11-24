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

- `main`: `b20e68b20ef5bec9c717f1e477eae064eec35a23`;
- `dev-cad`: `0b24df66481c43ff1cb798e749c728abd4ad6f33`;
- `dev-ci`: `ac47a97cbd2646f292c01c90f2defb95963e48bf`.

The complete post-v0.14 CAD/API batch is accepted on stable `main` through
history-preserving promotion #837 at
`b20e68b20ef5bec9c717f1e477eae064eec35a23`. Exact main durable run
`45398101329` succeeded and `build/main` source-matches that commit. The
earlier accidental #811 directory split remains fully reverted.

Latest published Forge package: **v0.14.0** at exact
`cd46d6797df319b9d13605c11568990113772700`.

The exact v0.14.0 main branch build `45381336046` and central release run
`45381885774` succeeded. Annotated tag object
`71464de5f5290a29b2b235ecf065b8bab35ad2c0` resolves to that exact source.
Forge v0.15.0 release preparation is active under #836.

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
- `docker.cad.solidcraft v0.3.5` / SolidCraft 0.48.1.

Pages is web output and is not release evidence. Stable release evidence is the
main **ci-build-record**.

## Active execution

### #836 — prepare and publish Forge v0.15.0

Status: **now / release**.

The complete post-v0.14 CAD/API batch was promoted history-preserving to stable
`main` as `b20e68b20ef5bec9c717f1e477eae064eec35a23`. Exact main durable run
`45398101329` succeeded and `build/main` source-matches that SHA.

v0.15.0 ships #347, #751 and #779 as public capability additions plus the #753
headless replay component-context fix. The release-preparation change is
metadata/documentation only: package version, dated changelog section, release
guidance and this plan. After it is merged, require exact candidate main durable
evidence before issuing the shared release command.


### #779 — native whole-sheet perforation

Status: **complete / durable-green on dev-cad**.

PR #780 merged through the repository policy as
`f87b93dd603b5dc808a3365638cdf39f6ec52d65`. Exact PR run `45386835984` and
durable dev-cad run `45387642616` both succeeded; #779 is closed.

### #347 — generalized native pattern seeds

Status: **complete / durable-green on dev-cad**.

PR #831 merged as `d8e310afa8766ee9b240f924d6dd8f6453c39c96`
after exact PR run `45389448588`; durable run `45390362018` also
succeeded and #347 is closed. Downstream CAD #135 still needs a Forge release
containing this state.

### #753 — restore component context across replay phases

Status: **implemented / owner-accepted; release and product render pending**.

PR #834 passed exact-head run `45395973854` and merged to dev-cad as
`5a1143e3f92136f880b14fe7f401f215391656cc`. Durable run `45396483792`
succeeded. The retained expanded component-cylinder occurrence output is
source-matched, and its durable preview was visually inspected: five intended
placed panel occurrences with no detached Cylinder/tool islands.

The generic fix restores active component context before any active-Sketch
restore when headless replay continues after a save/reopen checkpoint. These
restore commands remain transport-only and do not alter authored result/log
alignment.

Temporary downstream CAD #388 qualification run `45396787004` rebuilt all 16
consumer roots successfully, including `hub75-screen`, on the exact accepted
Forge fix with unchanged CAD geometry. Because the PR path does not publish its
generated PNG, final visual product acceptance stays after immutable v0.15.0
adoption on the normal durable CAD path. Keep #753 open until that render is
accepted.

### #751 — native exploded views

Status: **complete / included in v0.15.0 candidate**.

The native Assembly explode/show implementation is durable-green on dev-cad and
has been promoted to stable main. It preserves normal occurrence placement and
joint state while adding explicit presentation state. Downstream CAD #367 can
adopt it after the immutable v0.15.0 release.

### #788 — CAD-CI concurrency measurement

Status: **parallel / performance**.

Measure jobs=2/4/6 on one identical post-#785 representative full graph before
changing Forge concurrency or designing bounded batch sharding. Do not remove
Verification coverage or reintroduce per-model runtime startup.

## Open issue assessment

| Issue | Status | Next action |
| --- | --- | --- |
| #753 Component replay context across save/reopen | **release / product render pending** | Ship the accepted fix in v0.15.0; keep #753 open through final durable CAD #388 visual acceptance. |
| #788 Re-benchmark Forge CAD-CI concurrency | **parallel / performance** | Measure jobs=2/4/6 on one identical post-#785 full graph. |
| #779 Native whole-sheet perforation | **complete / v0.15.0 candidate** | Ship the accepted implementation in v0.15.0; issue already closed. |
| #751 Native exploded views | **complete / v0.15.0 candidate** | Ship in v0.15.0, then CAD #367 can consume the immutable release. |
| #737 Historical changelog alignment | **later / docs-only** | Keep separate from release behavior. |
| #713 Audit/reduce Forge scripts | **later** | Remove genuine duplicates only after owner migrations settle. |
| #659 Build/verification/results terminology | **later / cross-repo** | Follow the released shared terminology work; do not add Forge-local aliases. |
| #570 Remove CADCraft from verification diagrams | **later** | Preserve presentation while replacing the source format. |
| #349 Remaining SOLID CREATE coverage | **later** | Deliver focused reusable features when required. |
| #347 Generalized pattern seeds | **complete / v0.15.0 candidate** | Ship in v0.15.0, then CAD #135 can consume the immutable release. |
| #335 build123d Sheet Metal reference | **blocked upstream** | Wait for a released upstream Sheet Metal API. |
| #325 AnchorFrame root cause | **later / research** | Resume when an active product model requires the unresolved root-cause work. |
| #175 HUB75-like AnchorFrame diagnostic change | **later / diagnostic with #325** | Preserve the retained A/B evidence; resume its symbolic attached-seed/native comparison only as part of the #325 root-cause track. |
| #82 Joints-folder visibility | **later** | Decide interaction/export policy separately. |
| #81 Rotated occurrence-local AnchorFrame references | **later** | Investigate together with #325 when needed. |
| #9 First-class Sketch/constraints/workplanes | **later / epic** | Continue through focused qualified slices rather than one monolithic implementation. |
| #8 Hollow primitives | **later** | Reconcile with native shell/pipe support when a concrete model requires it. |
| #5 Generic anchors and parametric constraints | **later / foundational epic** | Treat as historical umbrella; continue only through focused issues with current native contracts. |

## Next checkpoint

1. validate and merge the #836 v0.15.0 release-preparation PR to `main`;
2. require the exact candidate main SHA's durable build and build record green;
3. publish only through `/release v0.15.0 <exact-sha>`;
4. verify annotated tag and GitHub Release resolve to that exact source;
5. let CAD #135/#367 consume the released capabilities and CAD #388 perform the
   final durable five-panel render acceptance before closing Forge #753;
6. keep #788 performance measurement independent from the release.
