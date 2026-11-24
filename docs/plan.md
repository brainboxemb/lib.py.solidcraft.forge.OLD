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

- `main`: `efc88bfcaf452051d721347f2e5ca561decad654`;
- `dev-cad`: `0b24df66481c43ff1cb798e749c728abd4ad6f33`;
- `dev-ci`: `ac47a97cbd2646f292c01c90f2defb95963e48bf`.

Latest published Forge package: **v0.15.0** at exact
`efc88bfcaf452051d721347f2e5ca561decad654`.

Release evidence:

- exact main durable run: `45399136016` — success;
- central release run: `45399592693` — success;
- annotated tag object:
  `1aa6304b412269163cffe19045cdd4b13b1f7e74`;
- tag target: exact v0.15.0 source above;
- runtime: `docker.cad.solidcraft v0.3.5` / SolidCraft 0.48.1.

The v0.15.0 batch contains #347 generalized native pattern seeds, #751 native
exploded Assembly presentation, #779 native whole-sheet perforation and #753
headless replay component-context restoration.

#753 is fully accepted downstream: CAD #388 adopted the immutable release as
`0d3081a1b76148854d82e2bf0e1593571fb7fb60`, durable run
`45400699265` succeeded, and the exact durable five-panel render was visually
clean. Both #753 and CAD #388 are closed.

After #839 is accepted on main, synchronize exact `main -> dev-cad`
history-preserving so the development lane starts from the recorded v0.15.0
baseline.

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

### #839 — record published v0.15.0 and synchronize the CAD lane

Status: **now / post-release administration**.

Record the immutable v0.15.0 source/tag/build/release and final #753 product
acceptance on stable `main`. After this docs-only change is durable-green,
synchronize exact `main -> dev-cad` through the normal history-preserving
permanent-lane path. Close #839 after the synchronized dev-cad durable build is
source-matched.

### #788 — CAD-CI concurrency measurement

Status: **next / performance**.

Measure `jobs=2`, `jobs=4` and, if runner resources remain healthy,
`jobs=6` on the same representative full Forge graph and same source. Current
consumer policy is explicit `jobs: 2` in all three calls in
`.github/workflows/scpf.yml`.

Record:

- total workflow wall time;
- CAD graph wall time;
- SolidCraft model-batch wall time;
- contract-test completion span;
- CPU/memory pressure or runner instability;
- runtime/container-start count.

Do not remove Verification coverage, reintroduce per-model runtime startup or
add a Forge-local scheduler. If a larger bounded job count captures most of the
gain safely, use the smallest effective value. Only design deterministic
SolidCraft batch sharding if the monolithic model batch remains the dominant
critical path.

## Open issue assessment

| Issue | Status | Next action |
| --- | --- | --- |
| #839 v0.15.0 post-release record | **now** | Merge docs-only record to main, then exact history-preserving main -> dev-cad sync and durable acceptance. |
| #788 Re-benchmark Forge CAD-CI concurrency | **next / performance** | Controlled jobs=2/4/6 A/B on identical source/full graph. |
| #737 Historical changelog alignment | **later / docs-only** | Keep separate from release behavior. |
| #713 Audit/reduce Forge scripts | **later** | Remove genuine duplicates only after owner migrations settle. |
| #659 Build/verification/results terminology | **later / cross-repo** | Follow released shared terminology work; do not add Forge-local aliases. |
| #570 Remove CADCraft from verification diagrams | **later** | Preserve presentation while replacing the source format. |
| #349 Remaining SOLID CREATE coverage | **later** | Deliver focused reusable features when required by real consumers. |
| #335 build123d Sheet Metal reference | **blocked upstream** | Wait for a released upstream Sheet Metal API. |
| #325 AnchorFrame root cause | **later / research** | Resume when an active product model requires the unresolved root cause. |
| #175 HUB75-like AnchorFrame diagnostic | **later / with #325** | Preserve retained A/B evidence; resume only as part of #325. |
| #82 Joints-folder visibility | **later** | Decide interaction/export policy separately. |
| #81 Rotated occurrence-local AnchorFrame references | **later** | Investigate with #325 when needed. |
| #9 First-class Sketch/constraints/workplanes | **later / epic** | Continue through focused qualified slices. |
| #8 Hollow primitives | **later** | Reconcile with native shell/pipe support when a concrete model requires it. |
| #5 Generic anchors and parametric constraints | **later / foundational epic** | Continue only through focused issues with current native contracts. |

## Next checkpoint

1. complete #839 on stable main;
2. synchronize exact `main -> dev-cad` history-preserving and require durable
   source-matched acceptance;
3. start #788 controlled jobs=2/4/6 measurement on one identical representative
   full Forge source/graph;
4. make no scheduler or batch-sharding change before the measurement evidence.
