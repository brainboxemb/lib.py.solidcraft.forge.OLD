# Forge repository plan

This file is the current source of truth for unfinished work in
`lib.py.solidcraft.forge`.

Forge is the central CAD library: public API, compiler/lowering, modelling
semantics, reusable CAD capabilities, examples and Forge-owned verification
expectations. Generic CAD-CI, generic CAD verification and runtime packaging
remain owned by their dedicated repositories.

## Current repository state

Permanent source refs:

```text
main
dev-cad
dev-ci
```

Current heads:

- `main`: `986a215a65bc1851cc7959d3555e228ebfaf91c7`;
- `dev-cad`: `ba8b6738dd3939d213dd5912ab74ce5a066f8e69`;
- `dev-ci`: `c393f2b238e51cc045bbae100cebb2af9b2be173`.

`dev-ci` has one legitimate unique commit (#738, tool.cad.ci 0.21.0
adoption) and is ten commits behind current `main`. Issue #741 / PR #742
exists only to restore current `main` ancestry before the #740 CI migration.

`dev-cad` remains on the separate CAD/history-reconciliation track under
#717/#721/#722. Do not overwrite it from CI work.

### Forge release

Current real package release: **v0.11.0** at
`9258d54079981604b6dd777a4c4face897c190fe`.

Issue #714 remains the explicit v0.12.0 release gate. Do not prepare or publish
v0.12.0 until the CAD/history track is reconciled, promoted and durable
`main`/stable Pages evidence is green.

### Generic CAD-CI owner baseline

Fully released and externally accepted owner stack:

- `lib.py.cad.ci 0.14.0` @
  `b24e9a3826dfc07e07b4f3fd9971fcb4ab5aa12d`;
- `tool.cad.ci v0.31.0` @
  `27bdf67077ddd485cea95ba199069249c20c2a46`;
- `tool.cad.ci.test` #223 completed real PR, durable publication,
  permanent-branch promotion/synchronization, merge-policy, exact-SHA
  retirement and cleanup acceptance for that exact release.

Forge has **not** fully adopted that owner baseline yet:

- default-branch merge governance still uses tool.cad.ci 0.20.1;
- `main` normal CAD-CI still uses the historical root composite action;
- `dev-ci` has the later historical root-action pin from #738;
- Forge still owns local PR classification and post-CAD-CI site/Page workflow
  steps that the current workflow/config model has replaced.

## Permanent branch rule

- `main`: stable integration only.
- `dev-cad`: Forge API/compiler/model/Verification/site-content work.
- `dev-ci`: CI/runtime/publication integration.
- Short-lived branches are squash-merged.
- Exact `dev-cad|dev-ci -> main`: normal history-preserving promotion.
- Exact `main -> dev-cad|dev-ci`: normal history-preserving synchronization.
- Merge mechanics come only from the exact released shared policy; Forge
  supplies branch roles and repository policy values.
- Generic CI/verification/runtime behavior is fixed/released in its owner repo
  before Forge adopts it.

## Active workstreams

### WS1 — migrate Forge CI to the accepted v0.31 workflow/config model

Status: **now**. Primary lane: governance/main, then `dev-ci`.

Required order:

1. #743 — move the thin default-branch merge-governance wrapper to exact
   tool.cad.ci v0.31.0 and the accepted public input names.
2. #741 / PR #742 — synchronize current `main -> dev-ci` with preserved
   history. PR #742 is currently a real conflict; after #743, use the released
   reviewed conflict-recovery path rather than a manual merge.
3. #740 — starting from the synchronized `dev-ci`, migrate Forge normal CI:
   - PR validation to released `reusable-ci.yml@v0.31.0`;
   - durable permanent-branch integration to
     `reusable-durable.yml@v0.31.0`;
   - remove Forge-local PR file/docs-only/full-run classification;
   - remove historical root-action calls;
   - make Forge site generation a normal CAD-CI item/builder output selected
     by root `cad-ci.yml:publication.pages`;
   - remove workflow-owned site build/Page publication post-steps;
   - keep `jobs=2` and Forge-owned site content/build implementation.
4. Qualify #740 on `dev-ci`, including durable `build/dev-ci` and
   `gh-pages/dev-ci` provenance.
5. Promote exact `dev-ci -> main` through the released v0.31 policy and
   require durable stable integration green.
6. Only after that stable CI cut-over, resume the dev-cad history/release track
   so shared documents are neutralized/synchronized once against the final CI
   baseline.

Do not fold #739 release-template migration into #740. It is a separate generic
Python-release consumer migration.

### WS2 — reconcile dev-cad history and prepare Forge v0.12.0

Status: **blocked on WS1 stable CI cut-over**.

- #717 / PR #721 — exact `main -> dev-cad` history synchronization.
- #722 — merge-neutral shared-document handling/restoration around that sync.
- #716 — exact `dev-cad -> main` promotion for the v0.12.0 candidate.
- #714 — explicit v0.12.0 release preparation/publication gate.

The existing exact permanent PRs #721 and #716 stay in place. Do not replace
them with temporary promotion/synchronization branches. Because `main` is now
moving for #743/#740, do not repeatedly re-neutralize dev-cad shared documents
until the stable CI cut-over is complete.

### WS3 — deferred infrastructure/documentation cleanup

- #739 released `tool.py.lib.ci` release-template adoption — **next after
  #740**, separate from CAD-CI migration.
- #737 historical changelog normalization — **later / docs-only**.
- #713 scripts ownership audit — **later**; reassess after the CI/release
  checkpoint.
- #659 build/verification/results terminology — **later**.
- #570 remove CADCraft from Verification diagrams — **later**.
- #335 build123d sheet-metal reference semantics — **later**.

### WS4 — API coverage and research

- #750 standalone Shape transform / local rotated cutter — **blocked on v0.12 checkpoint**;
  downstream CAD #362/#8 needs this to restore the final CornerBracket arm-tip
  wedge without a consumer-local transform workaround.
- #748 qualified STL export from accepted SolidCraft results — **blocked on v0.12 checkpoint**; downstream CAD #345 remains publication/adoption owner after an upstream release.
- #747 explicit/attached Sketch Polygon2D lowering — **blocked on v0.12 checkpoint**;
  downstream CAD #348 already owns the temporary compatibility workaround.
- #749 `run_script()` model-local import isolation — **blocked on v0.12 checkpoint**;
  downstream CAD #154 / draft PR #349 is the concrete consumer and must not
  carry a local `sys.modules` workaround.
- #349 remaining SOLID › CREATE coverage — **later**.
- #347 generalized pattern seeds — **later**.
- #325 AnchorFrame root-cause research — **later**.
- #81 rotated occurrence-local AnchorFrame references — **later**.
- #82 Joints-folder visibility — **later**.
- #9 first-class Sketch/constraints/workplanes — **later**.
- #8 hollow primitive intent — **later**.
- #175 — **probably obsolete**; consolidate useful evidence into #325.
- #5 — **probably obsolete** in current broad form; separate remaining
  constraint scope from #9.

## Open issue assessment — 2026-11-23

| Issue | Owner/lane | Status | Next action |
| --- | --- | --- | --- |
| #747 Support Polygon2D in explicit/attached Sketch compilation | dev-cad | **blocked on v0.12 checkpoint** | Required by CAD #348 to remove the temporary FlexBenchDog per-rib Slot workaround; implement only after current CI/history/release checkpoint permits a new CAD/API batch. |
| #748 Provide a qualified STL export path | dev-cad / runtime owner as needed | **blocked on v0.12 checkpoint** | Required by CAD #345; first determine the native SolidCraft/runtime export owner, then qualify STL from the accepted saved result without consumer STEP conversion. |
| #749 Isolate project-local modules between run_script roots | dev-cad | **blocked on v0.12 checkpoint** | Required by CAD #154 / draft PR #349; do not add consumer-local sys.modules cleanup. Implement after the current CI/history/release checkpoint permits a new CAD/API batch. |
| #750 Support local rotation/transform of standalone Shape cutters | dev-cad | **blocked on v0.12 checkpoint** | Required by CAD #362/#8 for the preserved CornerBracket arm-tip wedge; implement generically after the current release checkpoint. |
| #743 Adopt tool.cad.ci v0.31.0 merge governance | governance/main | **now** | Repin thin wrapper/test to v0.31 public names; merge to main. |
| #741 Synchronize main into dev-ci before #740 | repository/dev-ci | **blocked on #743** | Resolve PR #742 through v0.31 reviewed conflict recovery, then require dev-ci integration green. |
| #740 Migrate historical root action to workflow/config model | dev-ci | **blocked on #741** | Implement against synchronized dev-ci using exact accepted v0.31 workflows and publication config. |
| #739 Adopt tool.py.lib.ci release template | dev-ci | **next after #740** | Keep separate from CAD-CI migration. |
| #722 Normalize/restore shared documents around dev-cad sync | dev-cad | **blocked on #740 stable cut-over** | Re-neutralize only once against final stable CI docs, then restore after #721. |
| #721 #717 synchronize main history into dev-cad | repository/dev-cad | **blocked on #740/#722** | Keep exact main -> dev-cad PR; refresh after stable CI cut-over. |
| #717 Reconcile main/dev-cad history | repository/dev-cad | **blocked on #740** | Complete #722/#721 after CI migration reaches main. |
| #716 #714 promote dev-cad post-v0.11 batch | repository/main | **blocked on #717** | Keep exact dev-cad -> main PR; rerun after history sync/restoration. |
| #714 Release Forge 0.12.0 | repository | **blocked on #716** | Prepare/publish only after promoted main + durable evidence are green. |
| #737 Historical changelog alignment | docs | **later** | Do not mix retrospective changelog rewrite into release/CI cut-over. |
| #713 Audit/reduce Forge scripts | repository | **later** | Reassess after #740/#714; remove only truly generic duplicates. |
| #659 Standardize build/verification/results terminology | cross-repo | **later** | Schedule separately after architecture/release work stabilizes. |
| #570 Remove CADCraft from Verification diagrams | dev-cad | **later** | Preserve diagram responsibility while replacing CADCraft sources. |
| #349 Remaining SOLID › CREATE coverage | dev-cad | **later** | Split focused work only when a current model requires it. |
| #347 Patterns accept any applied Shape feature | dev-cad | **later** | Generalize seed validation by native feature identity. |
| #335 build123d Sheet Metal reference | dev-cad | **later** | Replace solid approximation with actual sheet-metal workflow. |
| #325 AnchorFrame regression root cause | dev-cad | **later** | Resume when it becomes an active model dependency. |
| #175 HUB75-like AnchorFrame diagnostic | dev-cad | **probably obsolete** | Consolidate useful evidence into #325, then close/rewrite. |
| #82 Joints folder visibility | dev-cad | **later** | Decide interaction/export policy later. |
| #81 Inline rotated AnchorFrame references | dev-cad | **later** | Investigate with #325. |
| #9 First-class Sketch/constraints/workplanes | dev-cad | **later** | Refresh epic and deliver focused slices. |
| #8 Tube/RectTube/OvalTube | dev-cad | **later** | Reconcile intent with native shell/pipe/boolean histories. |
| #5 Generic anchors/parametric constraints | dev-cad | **probably obsolete** | Separate remaining constraint scope from overlap with #9. |

## Boundary

Forge owns Forge-specific builders, site content and verification expectations.
Generic selection, SCons orchestration, durable build storage, Pages placement,
publication mechanics and merge governance remain in the released owner stack.

Do not recreate retired generic behavior locally while migrating consumers.

## Next release checkpoint

Finish #743 -> #741/#742 -> #740 -> v0.31 stable CI promotion first. Then
resume #721/#722/#717 -> #716/#714. Do not accumulate another CAD/API batch
before v0.12.0 is either published or explicitly deferred.
