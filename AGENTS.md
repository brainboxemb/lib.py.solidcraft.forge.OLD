# Forge repository architecture

This file summarizes the current repository structure. Historical documents may
describe earlier architecture.

## Repository role

`lib.py.solidcraft.forge` has two primary responsibility areas.

### 1. Forge CAD library

This repository owns the reusable Python Forge API, modelling semantics,
compiler/lowering, runners, unit tests, examples, native qualification and
model-specific verification fixtures.

Product CAD models are maintained in `2026-011-02.cad.solidcraft`, but missing
generic modelling capability discovered there belongs back in Forge when it is
part of the reusable CAD API/compiler contract.

### 2. CI and verification integration around Forge

This repository also owns how Forge consumes the released generic CAD-CI,
verification and SolidCraft runtime layers, plus its durable build/Page scopes
and Forge release integration.

Generic CI behavior itself belongs in `lib.py.cad.ci` / `tool.cad.ci`; generic
verification behavior belongs in `lib.py.cad.verification`; runtime packaging
belongs in `docker.cad.solidcraft`. Forge integrates those released owner-layer
capabilities but must not reimplement them locally.

## Current CI files

The active CI structure is defined by:

- `.github/workflows/scpf.yml`
- `.github/workflows/release.yml` — explicit owner-controlled package publication only
- `cad-ci.yml`
- `scpf/ci.yml`
- `ci/forge-tests/ci.yml`
- `ci/forge-release/ci.yml`
- `ci/release-policy/ci.yml` — tests release validation/publication policy without CAD runtimes
- `ci/builders/*/builder.yml` — Forge-owned executable repository builders
- migrated `examples/<model>/ci.yml` files
- `scripts/tool_ci.py`
- `scripts/tool_verify.py`
- `scripts/forge_example.py`
- `scripts/model_verification_batch.py`
- `scripts/model_verify_declarative.py`
- `scripts/release/validate_release.py`
- `scripts/release/publish_release.py`

The generic planner/executor is `tool.cad.ci`.

Forge model items declare item-level `process` state in
`examples/<model>/ci.yml`. The reconciled catalog contains 36 active model-verification items: the final
32 historical cases plus four restored historical native cases from #559.
`model_authoring` remains an explicit Q1/Q2-only regression fixture. Forge does not interpret `process`; released `tool.cad.ci` /
`lib.py.cad.ci` own its selection and execution semantics.

## Current verification steps

Forge package CI is split into independent items:

```text
forge-package
  ├─ forge-tests
  ├─ forge-release
  └─ model-verification-batch
       └─ examples/<model> native SolidCraft verification

CAD-CI verification-package capability
  ├─ model-verification-batch builder (verification_package: true)
  ├─ reference-verification-batch builder (verification_package: true)
  └─ built-in reference runtime
       ├─ CadQuery reference items
       └─ build123d reference items
```

The arrows mean dependency ownership, not one serial release chain.

- `forge-package` builds the exact SCPF wheel once.
- `forge-tests` installs that wheel and runs the reusable Forge unit suite.
- `forge-release` release-verifies that wheel with the fixed representative
  examples.
- declarative model items depend on `forge-package` and the shared
  `model-verification-batch`; the batch consumes the CAD-CI-owned exact
  verification package.
- CadQuery/build123d reference items use the released built-in builders plus
  first-class `mesh-geometry` verification directly.
- PythonSCAD/pyBOSL2 reference items remain Forge-owned and project results from
  `reference-verification-batch`.

Model verification must not depend on `forge-tests` or `forge-release`.
Those are independent checks.

Migrated model items use `model_verify`. That step compiles the model with the
exact built Forge wheel, produces the initial native SolidCraft model and then
delegates verification to released `lib.py.cad.verification`.

A model keeps only model-specific verification data in
`verification/verify.py`; it does not own a procedural verification CLI.
All current model items use the declarative verification path, have native
`model_verify` coverage and own model-local independent-reference geometry
contracts. Generic build123d/CadQuery export and mesh verification are not
implemented in Forge.

The catalog lineage and the additional non-catalog fixtures below `examples/`
are documented in `docs/background/example-history.md`.

## Model ownership

A declaratively migrated model may contain:

```text
examples/<model>/
  ci.yml
  model.yml
  README.md
  scpf/
    model.py
  verification/
    verify.py
    <model-specific command/data files>
```

All current historical model-verification cases use
`verification/verify.py`. Do not add new procedural per-model verification
CLIs; reusable verification mechanics belong in the released verification
library.

Presentation metadata in `model.yml` uses the canonical reusable contract in
`scpf.model_metadata` and the exact template in `docs/templates/model.yml`:

```text
purpose
section
priority
title
tagline
description
parameters
stages
```

Consumers must reuse `validate_model_metadata()` rather than copying this field
list or validator. `model.yml` has no consumer-specific extension fields.

`model.yml` is the generic model/page metadata source. `purpose` classifies a model as `example`, `verification`, or both through a YAML list. It is the only public Example/Verification membership interface. `priority` is presentation-only ordering within the declared section; lower values render first. The example
`README.md` owns human engineering explanation such as the goal, Forge API
and model, SolidCraft lowering/result, saved-design explanation, geometry
sufficiency rationale and reference notes. Do not infer or summarize those
statements during source migrations.

Exact verification values remain in `verification/verify.py`; actual current
results come from durable `build/main`. Do not add a central Python example
page catalog.

Repository-local `role.yml` files may remain as historical fixture notes, but
they are not a public catalog interface and their presence or absence must not
decide Example/Verification membership. Do not add `catalog.yml`, a central
hand-authored membership registry or directory-name semantics; use canonical
`model.yml.purpose`.

Native-model expectations and mutation definitions live as model-specific data
in the model verification definition.
Example-owned command-contract tests remain under `examples/<example>/tests/`
where they are used by Forge release verification or other focused tests.

## SolidCraft runtime

The reusable SolidCraft CAD runtime is owned, built and released by
`brainboxemb/docker.cad.solidcraft`.

Forge is a consumer only. Root `cad-ci.yml` selects the immutable released
runtime role images:

```text
FORGE_RUNTIME_IMAGE=ghcr.io/brainboxemb/cad-solidcraft:v0.3.4
REFERENCE_RUNTIME_IMAGE=ghcr.io/brainboxemb/cad-reference:v0.3.4
```

Normal SolidCraft model/visual verification uses only
`FORGE_RUNTIME_IMAGE`. Forge-owned PythonSCAD/pyBOSL2 reference work uses
`REFERENCE_RUNTIME_IMAGE`. Built-in CadQuery/build123d references use the
root `runtimes.reference` role owned by released `lib.py.cad.ci`.

Forge must not duplicate the runtime Dockerfile, dependency/version pins or
release workflow. Runtime package composition, role boundaries and release
management belong in `docker.cad.solidcraft`.

The runtime images must not embed `lib.py.cad.verification`. Root `cad-ci.yml`
pins the exact released verification package. Forge-owned repository builders
request the released `verification_package: true` capability and consume the
validated wheel only through `CAD_CI_VERIFICATION_WHEEL`. Built-in CAD
verification uses the same owner-managed package. Forge must not name CAD-CI's
internal synthesized item or build/transport another verification wheel.

Changing the verification-library pin or a model-local `verification/verify.py`
must not require a Docker runtime release.

`scpf/scpf/version.py::TESTED_SOLIDCRAFT_VERSION` remains Forge's package-level
compatibility guard. Root `cad-ci.yml` keeps the explicit SolidCraft version
expected by Forge CI.

Version-pinned SolidCraft engineering references live under
`docs/reference/solidcraft/<version>/`. Before targeting a newer SolidCraft
release, add a new sibling version directory with exact upstream provenance and
capture the version-specific reference material before compatibility changes.
Never overwrite an already qualified version directory. The procedure is in
`docs/development.md`.

## Test ownership

- `scpf/tests/` — reusable Forge API/compiler tests.
- the fixed release examples — Forge `tool_verify`.
- `examples/<model>/verification/` — native SolidCraft model checks.

`docs/background/design/test-architecture.md` contains the detailed test split.

## Public API documentation

The primary API contract is `docs/api.md`.

Exact public names, signatures, defaults and enum values come from the Python
implementation and its docstrings. Cross-object semantic rules live in
`docs/api.md`; documentation-generation/development rules live in
`docs/development.md`.

`docs/agent/forge-api.json` is generated from the same public API sources.
Do not maintain a second handwritten API manual in `scpf/README.md`, AGENTS,
or the agent directory.

Historical documentation-architecture discussion is preserved under
`docs/background/documentation-architecture.md`.

## Current work and handoff protocol

The canonical session handoff is `docs/handoff.md`, following the shared
`brainboxemb/meta.cad.solidcraft/templates/docs/handoff.md` structure.

A handoff is only an entrypoint. Never treat copied handoff text as fresher than
GitHub or the repository plan. A handoff must also keep both active repository
areas visible: CAD-library work and CI/infrastructure work. Do not describe the
repository as if it were only a CI project.

For every work session:

1. inspect current issues, PRs and branches;
2. read this `AGENTS.md` and `docs/plan.md`;
3. treat `docs/plan.md` as the source of truth for unfinished work;
4. create an issue before implementation when the logical change has none;
5. update the plan before implementation and reassess every open issue as
   `now`, `next`, `later`, `blocked`, `probably obsolete` or
   `effectively complete but still open`;
6. update requirements/design documents when behavior or architecture changes;
7. only then change code;
8. keep one logical change to one issue, branch and PR;
9. after merge or release, reconcile the plan again.

Do not serialize independent work unnecessarily. `dev-cad` and `dev-ci` may
advance in parallel; wait for a workflow only when the next step actually
depends on its result. Shared dependency releases and architecture gates remain
synchronization points. Repository-wide governance may use a short branch
directly against `main`.

`docs/plan.md` contains unfinished repository work. Completed plan sections are
removed after their corresponding change is merged, while still-open completed
issues are explicitly classified until they are closed.

## Generated output, branches and Pages

Forge has three permanent source branches:

```text
main
dev-cad
dev-ci
```

Branch roles are fixed:

- `main` — stable integration only;
- `dev-cad` — Forge API/compiler/model/Verification/site-content work;
- `dev-ci` — Forge CI/infrastructure/publication integration.

Generic CAD-CI behavior still belongs in `lib.py.cad.ci` /
`tool.cad.ci` first. Forge consumes exact released generic behavior; do not
implement a Forge-local planner, build store, merge policy or generated-branch
mutator.

Short-lived work branches target one dev lane and are squash-merged. Their PRs
are verification-only and must not publish durable PR build/Page state.

The two development lanes are independent execution tracks. Continue unrelated
work in the other lane while one lane validates or publishes; a running workflow
is a gate only for work that depends on its result. Repository-wide governance
that applies equally to both lanes may use a short-lived branch directly against
`main`.

Do not select a PR merge method manually. Use the repository `/merge`
wrapper, which delegates the mechanical policy to the exact externally
accepted tool.cad.ci reusable merge-policy workflow.

The released policy has three explicit classes:

- base `main` + head exactly `dev-cad` or `dev-ci` -> normal merge
  promotion; the promoted lane is preserved/advanced at the resulting main
  merge commit;
- base exactly `dev-cad` or `dev-ci` + head `main` -> normal
  history-preserving stable-to-lane synchronization; `main` is not mutated by
  branch-lifecycle handling;
- every other supported PR -> squash merge.

Forge supplies branch names, permanent refs, cleanup prefixes and `scpf.yml`
integration dispatch only; it does not implement the decision/API calls locally.
Both permanent-direction operations require a same-repository head.
Same-head GitHub Actions runs triggered by `issue_comment` are command workflows,
not PR validation checks; the released policy filters them by Actions-run identity
while keeping normal validation checks and commit statuses mandatory.

Temporary `promote/*` heads are not part of the supported promotion flow.
Merged short-lived branches are removed only through the policy cleanup
allow-list; permanent/generated/backup refs are never cleanup targets.

Durable accepted output lives on generated `build`:

```text
main/
dev-cad/
dev-ci/
```

Generated Pages lives on one `gh-pages` branch:

```text
/           <- main stable site
/dev-cad/   <- dev-cad preview
/dev-ci/    <- dev-ci preview
```

Merge governance and normal Forge PR/durable CAD-CI execution consume exact
externally accepted `tool.cad.ci v0.35.0` at
`9fcad92b7c5f10ae29a9cb085a4f25bb38ed00f9`, which pins
`lib.py.cad.ci v0.18.2` at
`088644a05ff698957aef2ddc6cc5de037ddfa158`. Merge governance keeps the
public branch-role inputs and supports both normal `/merge` and reviewed
`/merge-resolved` conflict recovery. Normal CI uses the released reusable
PR/durable workflows with `jobs=2`; Forge does not own PR classification,
durable build-store mechanics or Pages publication.

Do not reintroduce Actions artifact transport, a second publication runner, a
second tool/library bootstrap, or Forge-owned selection/build-store logic.

For named dev lanes, incremental selection uses the previous `source_commit`
recorded in that lane's durable `build.json` manifest as the base. Do not assume
`github.event.before` is valid: branch recreation events use an all-zero
before SHA.

Promotion remains direct from the accepted long-lived lane:

```text
dev-cad -> PR main
dev-ci  -> PR main
```

When a lane has fallen behind `main` and ancestry must be restored before
promotion, synchronization is also direct between permanent refs:

```text
main -> PR dev-cad
main -> PR dev-ci
```

Both paths run normal PR validation and are merged only through `/merge`.
Promotion advances/preserves the promoted lane at the main merge commit.
Stable-to-lane synchronization updates the lane by normal merge and leaves the
stable source ref unchanged.

All other PRs, including governance and any temporary `promote/*` heads, are
squash-merged by the same policy workflow.

Site Python code may discover/load/validate/render data, but complete
hand-authored pages and guide prose belong in external templates/content, not
Python string literals.

Generated GitHub Pages publication is live. The stable root represents `main`
and `/dev-cad/` and `/dev-ci/` are lane previews. Issue #366 is complete and
must not be treated as an active publication gate.

## Release state

The package version is stored in `scpf/pyproject.toml`, but source metadata is
not release evidence.

The latest actual Forge release is **`v0.11.0`**, published from exact source
commit `9258d54079981604b6dd777a4c4face897c190fe`. The annotated tag and
GitHub Release both resolve to that commit. Source package version `0.11.0` is
therefore the released baseline; new user-visible work remains under the fresh
`[Unreleased]` changelog section.

Issue #642 is complete. The authoritative procedure for future releases is
`docs/release.md`.

Normal Forge CI verifies candidates and publishes durable build/Page state; it
never creates a release automatically. Publication is the separate owner-only
`/release vX.Y.Z <exact-main-sha>` path documented in `docs/release.md`.
A release exists only after the immutable annotated tag and GitHub Release are
both verified against the intended green `main` SHA.

The next planned release checkpoint is v0.12.0 after the first coherent
post-v0.11 CAD/CI batch; do not bump source metadata or create its dated
changelog section before an explicit release issue/gate exists.

Issue #366 is complete and is not a release blocker.

## Historical documents

`docs/background/changes/` and several older audit/remediation documents under
`docs/background/design/` describe earlier development states. Their old terminology is
historical rather than an active CI contract.

## Documentation structure

The primary human documents are:

- `docs/api.md`;
- `docs/design.md`;
- `docs/development.md`;
- `docs/plan.md`;
- `docs/requirements.md`;
- `docs/release.md`.

Current task guidance belongs under `docs/manual/`. Current version-pinned
external engineering references belong under `docs/reference/`. Historical or
narrow design, change, audit, migration and superseded research records belong
under `docs/background/`. Generated machine-oriented API data remains under
`docs/agent/`.

## Repository plan

`docs/plan.md` is the current source of truth for unfinished repository work.

Keep it as a current snapshot, not as historical documentation:

- state the current goal and execution order;
- include every open issue in an issue assessment snapshot;
- give each open issue an explicit status such as `now`, `later`, `blocked`, `probably obsolete`, or `effectively complete but still open`;
- explain briefly why that status applies;
- identify dependencies or blockers between issues;
- remove completed work from the active execution sections after merge/release, while keeping the issue assessment current.

Issues contain detail and history. README and design/requirements documents describe stable purpose and behavior. The plan tells an agent what work is actually current and what should happen next.



### Verification cut-over compatibility

Canonical public content stays under `verification/`. Do not reintroduce a
second authored Qualification site.

The pre-cut-over `qualification/` output is generated compatibility only:
redirect HTML, the current Verification manifest alias and legacy
joint-anatomy CadCraft JSON aliases.

The standalone Results page comes from durable evidence; Coverage comes from
`site/api_coverage.py` + `site/capability_map.py`; Joint anatomy human prose
belongs in its external template and its diagrams remain owned by
`verification/diagrams/sources/`. Do not move those complete pages into
Python strings.
