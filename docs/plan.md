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

- `main`: `cd46d6797df319b9d13605c11568990113772700`;
- `dev-cad`: `d8e310afa8766ee9b240f924d6dd8f6453c39c96`;
- `dev-ci`: `ac47a97cbd2646f292c01c90f2defb95963e48bf`.

Forge #785 / PR #816 is accepted on `dev-cad`. Exact durable branch run
`45358578565` succeeded and published the accepted dev-cad build/Page state.
The earlier accidental #811 directory split is fully reverted and is not part
of the active architecture.

Latest published Forge package: **v0.14.0** at exact
`cd46d6797df319b9d13605c11568990113772700`.

The exact v0.14.0 main branch build `45381336046` and central release run
`45381885774` succeeded. Annotated tag object
`71464de5f5290a29b2b235ecf065b8bab35ad2c0` resolves to that exact source.
No Forge release is currently active.

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

### #779 — native whole-sheet perforation

Status: **complete / durable-green on dev-cad**.

PR #780 merged through the repository policy as
`f87b93dd603b5dc808a3365638cdf39f6ec52d65`. Exact PR run `45386835984` and
durable dev-cad run `45387642616` both succeeded; #779 is closed.

### #347 — generalized native pattern seeds

Status: **merged to dev-cad**.

PR #831 merged as `d8e310afa8766ee9b240f924d6dd8f6453c39c96`
after exact PR run `45389448588` succeeded. Downstream CAD #135 may refresh
after the normal durable dev-cad acceptance.

### #753 — component-local Cylinder history across occurrences

Status: **reopened / primary product-CAD blocker**.

CAD #388 consumed released Forge v0.14.0 and runtime v0.3.5 / SolidCraft 0.48.1.
Its exact durable run `45389479040` succeeded, but the source-matched five-panel
render still shows multiple detached joined-Cylinder features. The accepted
Box+one-Cylinder fixture and v0.3.5 two-island smoke are therefore insufficient.

Retain the owner boundary: no CAD-local geometry workaround. Expand the Forge
reproducer to preserve the actual failing history shape — taper/rear cut,
multiple Cylinder joins and Hole features, five copied/rotated occurrences —
until the failure reproduces under the same 0.48.1 runtime. Then reduce the
sequence to the smallest failing difference and move the fix to the owning
Forge/SolidCraft layer.

### #788 — CAD-CI concurrency measurement

Status: **parallel / performance**.

Measure jobs=2/4/6 on one identical post-#785 representative full graph before
changing Forge concurrency or designing bounded batch sharding. Do not remove
Verification coverage or reintroduce per-model runtime startup.

## Open issue assessment

| Issue | Status | Next action |
| --- | --- | --- |
| #753 Component-local Cylinder history across occurrences | **now / primary blocker** | Reproduce the actual HUB75 multi-feature failure on SolidCraft 0.48.1 and isolate the smallest failing sequence. |
| #788 Re-benchmark Forge CAD-CI concurrency | **parallel / performance** | Measure jobs=2/4/6 on one identical post-#785 full graph. |
| #779 Native whole-sheet perforation | **complete / durable-green** | Accepted at `f87b93dd603b5dc808a3365638cdf39f6ec52d65`; issue closed. |
| #751 Native exploded views | **next / CAD unblocker** | After #347, expose native explode.create/show for CAD #367. |
| #737 Historical changelog alignment | **later / docs-only** | Keep separate from release behavior. |
| #713 Audit/reduce Forge scripts | **later** | Remove genuine duplicates only after owner migrations settle. |
| #659 Build/verification/results terminology | **later / cross-repo** | Follow the released shared terminology work; do not add Forge-local aliases. |
| #570 Remove CADCraft from verification diagrams | **later** | Preserve presentation while replacing the source format. |
| #349 Remaining SOLID CREATE coverage | **later** | Deliver focused reusable features when required. |
| #347 Generalized pattern seeds | **merged / durable acceptance pending** | Refresh CAD #135 after normal dev-cad acceptance. |
| #335 build123d Sheet Metal reference | **blocked upstream** | Wait for a released upstream Sheet Metal API. |
| #325 AnchorFrame root cause | **later / research** | Resume when an active product model requires the unresolved root-cause work. |
| #175 HUB75-like AnchorFrame diagnostic change | **later / diagnostic with #325** | Preserve the retained A/B evidence; resume its symbolic attached-seed/native comparison only as part of the #325 root-cause track. |
| #82 Joints-folder visibility | **later** | Decide interaction/export policy separately. |
| #81 Rotated occurrence-local AnchorFrame references | **later** | Investigate together with #325 when needed. |
| #9 First-class Sketch/constraints/workplanes | **later / epic** | Continue through focused qualified slices rather than one monolithic implementation. |
| #8 Hollow primitives | **later** | Reconcile with native shell/pipe support when a concrete model requires it. |
| #5 Generic anchors and parametric constraints | **later / foundational epic** | Treat as historical umbrella; continue only through focused issues with current native contracts. |

## Next checkpoint

1. reproduce CAD #388 in the retained #753 owner-layer fixture using the real
   multi-feature HUB75 history shape on runtime v0.3.5 / SolidCraft 0.48.1;
2. reduce that reproducer to the smallest failing sequence and fix/block it at
   the owning Forge/SolidCraft layer; do not add a product-CAD workaround;
3. keep #751 exploded views and #788 performance work parallel where they do
   not interfere with #753;
4. refresh downstream CAD #135 after #347 durable acceptance.
