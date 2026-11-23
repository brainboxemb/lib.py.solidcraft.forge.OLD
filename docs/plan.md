# Forge repository plan

This file is the current source of truth for unfinished work in
`lib.py.solidcraft.forge`.

Forge owns the public CAD library/compiler/model semantics, Forge-specific
verification expectations, presentation policy and repository-specific builder
commands. Generic CAD-CI, reusable CAD verification, runtime packaging,
durable build state, Pages publication and merge governance stay in their owner
repositories.

## Current repository state

Permanent source refs:

```text
main
dev-cad
dev-ci
```

Current heads at #740 start:

- `main`: `e2025214fed3d9abaa7fa9bc5a20f71972465715`;
- `dev-cad`: `ba8b6738dd3939d213dd5912ab74ce5a066f8e69`;
- `dev-ci`: `685afbc3c925f951c5d69cb883429a805b85eb2d`.

`main` and `dev-ci` currently differ in source only by `docs/plan.md`;
their history is divergent but #740 can proceed safely on the synchronized
`dev-ci` implementation baseline without touching dev-cad.

Existing permanent PRs #721 (`main -> dev-cad`) and #716
(`dev-cad -> main`) remain intentionally open and blocked until the stable
CI cut-over is complete. Do not replace them with temporary promotion/sync
branches.

### Forge package release

Current real Forge package release: **v0.11.0** at
`9258d54079981604b6dd777a4c4face897c190fe`.

Issue #714 remains the explicit v0.12.0 release gate. The dev-cad CAD/API batch
must not be promoted/released until the CI cut-over is stable, dev-cad history
is synchronized/restored and durable main/Pages evidence is green.

### Accepted generic owner stack

- `lib.py.cad.ci v0.18.2` @
  `088644a05ff698957aef2ddc6cc5de037ddfa158`;
- `tool.cad.ci v0.35.0` @
  `9fcad92b7c5f10ae29a9cb085a4f25bb38ed00f9`;
- `lib.py.cad.verification v0.16.0` @
  `c7c145b7be0c602724e8cca874ef29990baaad1e`;
- `docker.cad.solidcraft v0.3.4` immutable SolidCraft/reference runtimes;
- external acceptance complete through `tool.cad.ci.test #248`: existing
  CadQuery Workplane root 017 and new Assembly root 019 both pass on the
  released v0.35.0/v0.18.2 stack, followed by green dev-ci, main and dev-cad
  durable provenance.

## Permanent branch rule

- `main`: stable integration only.
- `dev-cad`: Forge API/compiler/model/Verification/site-content work.
- `dev-ci`: CI/runtime/publication integration.
- short-lived branches are squash-merged;
- exact `dev-cad|dev-ci -> main`: history-preserving normal merge;
- exact `main -> dev-cad|dev-ci`: history-preserving normal merge;
- merge mechanics come only from the exact released shared policy;
- generic CI/verification/runtime behavior is changed/released in the owner repo
  before Forge adopts it.

## Active workstreams

### WS1 — #740 CAD-CI v0.35.0 cut-over

Status: **now**. Lane: `dev-ci`.

The released v0.35.0 workflow adds read-only targeted selection. Qualify this
migration in explicit gates without toggling model `process` state:

1. one representative model: `simple-box`;
2. five model source paths in one graph;
3. ten model source paths in one graph;
4. remove the temporary selector and run the full catalog.

Only advance when the previous gate is green. The 5/10 gates use public
`changed_paths` input so shared direct-dependent batches are exercised in the
same graph. External selector acceptance is complete in
`tool.cad.ci.test #254` (runs `45217000064` and `45217425529`).

Required order:

1. replace `.github/workflows/scpf.yml` with the released v0.35.0 lane
   workflow shape, preserving `jobs=2`;
2. move Forge Pages generation to a repository-owned post-build Pages builder
   using the CAD-CI complete-scope/source/build provenance environment;
3. move executable item/template steps into repository-owned
   `ci/builders/*/builder.yml` implementations;
4. add the root exact `lib.py.cad.verification v0.16.0` package pin and
   remove Forge's generic verification-package producer/transport;
5. move build123d/CadQuery reference build + mesh verification to the built-in
   generic builders;
6. retain only Forge-owned SolidCraft verification, visual/presentation policy
   and PythonSCAD/pyBOSL2 behavior;
7. update site evidence/rendering so Forge presentation can consume the new
   accepted durable generic reference outputs without recreating generic
   geometry verification;
8. require exact-head PR CI green, merge to `dev-ci`, and require real durable
   `build/dev-ci` + `gh-pages/dev-ci` provenance green;
9. promote exact `dev-ci -> main` through the released merge policy and
   require stable durable integration green.

Do not fold #739 Python-release-template work into #740.

### WS2 — resume dev-cad history and Forge v0.12.0

Status: **blocked on WS1 stable cut-over**.

After #740 reaches stable `main`:

1. #722 — refresh merge-neutral shared documentation once against the final CI
   baseline;
2. #721 / #717 — synchronize exact `main -> dev-cad`;
3. restore the preserved dev-cad-only CAD documentation;
4. #716 — promote exact `dev-cad -> main`;
5. #714 — prepare/publish Forge v0.12.0 through the explicit release gate.

### WS3 — subsequent infrastructure/documentation work

- #739 released `tool.py.lib.ci` release-template adoption — **next after
  #740**, separate issue.
- #713 scripts ownership audit — **later**, but #740 may delete scripts that
  become unambiguously obsolete because owner functionality has replaced them.
- #737 historical changelog normalization — **later / docs-only**.
- #659 build/verification/results terminology — **later**.
- #570 CADCraft diagram replacement — **later**.
- #335 build123d Sheet Metal reference semantics — **later**.

### WS4 — CAD/API work after the release checkpoint

Issues #746, #747, #748, #749, #750 and #751 are real reusable Forge gaps but
are **blocked on the current #740/history/v0.12 checkpoint**. Do not accumulate
another CAD/API release batch before v0.12.0 is either published or explicitly
deferred.

Other longer-term API/research work remains later: #349, #347, #325, #81, #82,
#9 and #8. #175 and #5 remain probably obsolete in their current broad forms.

## Open issue assessment — 2026-11-23

| Issue | Owner/lane | Status | Next action |
| --- | --- | --- | --- |
| #740 CAD-CI v0.35.0 workflow/config + generic builder migration | dev-ci | **now** | Complete owner-stack cut-over on the externally accepted v0.35.0/v0.18.2 pair, durable dev-ci acceptance, then stable promotion. |
| #739 Adopt tool.py.lib.ci release template | dev-ci | **next after #740** | Keep separate from CAD-CI migration. |
| #722 Normalize/restore shared docs around dev-cad sync | dev-cad | **blocked on #740 stable cut-over** | Refresh once against final stable CI baseline, then restore after #721. |
| #717 Reconcile main/dev-cad history | dev-cad | **blocked on #740** | Complete #722/#721 after CI migration reaches main. |
| #714 Release Forge 0.12.0 | repository | **blocked on #717/#716** | Prepare/publish only after promoted main and durable evidence are green. |
| #746 Cone join/cut feature compilation | dev-cad | **blocked on v0.12 checkpoint** | Reusable compiler gap; implement in the next CAD/API batch. |
| #747 Polygon2D explicit/attached Sketch compilation | dev-cad | **blocked on v0.12 checkpoint** | Required by downstream CAD; no consumer workaround. |
| #748 Qualified STL export path | dev-cad/runtime owner | **blocked on v0.12 checkpoint** | Determine native export owner, then qualify released path. |
| #749 Isolate project-local modules between run_script roots | dev-cad | **blocked on v0.12 checkpoint** | Fix runner ownership, no consumer sys.modules workaround. |
| #750 Standalone Shape local transform/rotation | dev-cad | **blocked on v0.12 checkpoint** | Add generic cutter transform support after release checkpoint. |
| #751 Native SolidCraft exploded views | dev-cad | **blocked on v0.12 checkpoint** | Wrap/qualify native explode API after release checkpoint. |
| #713 Audit/reduce Forge scripts | repository | **later** | Reassess after #740/#714; remove only genuine duplicates. |
| #737 Historical changelog alignment | docs | **later** | Do not mix retrospective rewrite into CI/release cut-over. |
| #659 Standardize build/verification/results terminology | cross-repo | **later** | Separate follow-up. |
| #570 Remove CADCraft from Verification diagrams | dev-cad | **later** | Preserve presentation responsibility while replacing source format. |
| #349 Remaining SOLID › CREATE coverage | dev-cad | **later** | Focused slices only when needed. |
| #347 Generalized pattern seeds | dev-cad | **later** | Generalize by native feature identity. |
| #335 build123d Sheet Metal reference | dev-cad | **later** | Replace solid approximation with real sheet-metal reference. |
| #325 AnchorFrame root cause | dev-cad | **later** | Resume when an active model requires it. |
| #175 HUB75-like AnchorFrame diagnostic | dev-cad | **probably obsolete** | Consolidate useful evidence into #325. |
| #82 Joints-folder visibility | dev-cad | **later** | Decide interaction/export policy later. |
| #81 Rotated occurrence-local AnchorFrame references | dev-cad | **later** | Investigate with #325. |
| #9 First-class Sketch/constraints/workplanes | dev-cad | **later** | Refresh epic and deliver focused slices. |
| #8 Hollow primitives | dev-cad | **later** | Reconcile with native shell/pipe/boolean histories. |
| #5 Generic anchors/parametric constraints | dev-cad | **probably obsolete** | Separate any remaining scope from #9. |

## Boundary

Forge may own:

- Forge-specific builder commands;
- model-specific SolidCraft verification definitions;
- visual/presentation policy;
- site content/rendering.

Forge must not own:

- generic PR diff/docs classification;
- CAD-CI planning/SCons/cache behavior;
- built-in build123d/CadQuery runtime batching;
- reusable mesh geometry verification;
- verification-package materialization/transport;
- durable build-store semantics;
- Pages placement/publication mechanics.

## Next release checkpoint

Finish #740 through stable promotion first. Then complete
#722/#721/#717 -> #716/#714. Do not start a new CAD/API implementation batch
before Forge v0.12.0 is published or explicitly deferred.
