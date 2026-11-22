# Forge requirements

This document records stable repository requirements. Cross-object API behavior is documented in `docs/api.md`; exact public
signatures/defaults remain implementation/docstring-owned.

## CI ownership

- `tool.cad.ci` is the only generic CAD-CI planner/executor.
- Forge workflows remain thin orchestration.
- Forge owns Forge compilation, model definitions and model-specific
  expectation data.
- Shared verification behavior comes from released
  `lib.py.cad.verification`, including CAD-tool-specific adapters such as the
  SolidCraft adapter.

## Forge release publication

Forge release verification and Forge release publication are separate actions.

Requirements:

- a green CAD-CI run must never publish a Forge release automatically;
- publication is an explicit repository-owner operation;
- the publication request names both the semantic version and one exact
  40-character `main` commit SHA;
- that SHA must still be the current `main` head when publication executes;
- package metadata, the dated changelog section and
  `TESTED_SOLIDCRAFT_VERSION` are read from that exact SHA;
- `docs/background/design/release-blockers.txt` must contain no active
  non-comment blocker;
- durable `build/main/build.json` must name that SHA as its source commit and
  its `ci/forge-release` item must have been produced from that same SHA;
- stable `gh-pages/provenance.json` must name that SHA as both site source and
  build-manifest source;
- publication creates an annotated `vX.Y.Z` Git tag and a GitHub Release only
  after all of those checks pass;
- an existing tag may only be reused when it resolves to the exact requested
  SHA; a conflicting tag or existing mismatched release is a hard failure;
- the release workflow is a thin owner-only trigger; validation and release-note
  extraction live in repository code under `scripts/release/`;
- publication must not modify `main`, `dev-cad`, `dev-ci`, `build` or
  `gh-pages`.

A package-version literal, changelog heading, successful verification run or
commit message containing the word “release” is not release evidence by itself.
A release is complete only when the immutable tag and GitHub Release both exist
for the validated SHA.

## SolidCraft runtime ownership

The reusable SolidCraft CAD runtime is owned by
`brainboxemb/docker.cad.solidcraft`.

Forge is a consumer only.

Therefore Forge must not own or duplicate:

- the runtime Dockerfile;
- runtime dependency/version pins;
- runtime image build/publication workflows;
- runtime release/version management.

Root `cad-ci.yml` declares the exact immutable released role images Forge
consumes:

```text
FORGE_RUNTIME_IMAGE=ghcr.io/brainboxemb/cad-solidcraft:vX.Y.Z
REFERENCE_RUNTIME_IMAGE=ghcr.io/brainboxemb/cad-reference:vX.Y.Z
```

Both roles must use the same immutable runtime release. The exact current
consumer values live in root `cad-ci.yml`; this requirements document does not
duplicate the moving release number.

Changing either runtime role is a two-repository operation:

1. change, test and release a new immutable version from
   `docker.cad.solidcraft`;
2. deliberately update Forge's corresponding immutable role image.

Forge never derives a runtime version from source hashes, timestamps or local
Docker files.

## Runtime consumption

Forge CAD-CI commands read the injected repository environment:

- `FORGE_RUNTIME_IMAGE` is the exact immutable released SolidCraft
  model/visual verification image;
- `REFERENCE_RUNTIME_IMAGE` is the exact immutable released independent
  reference-engine image;
- `SOLIDCRAFT_VERSION` is the SolidCraft version expected by Forge CI.

Model verification must not use the reference image. Independent reference
verification must not use the SolidCraft image.

Consumer commands do not parse `cad-ci.yml` themselves.

A missing released image is an error. Forge CI must not build or publish a
runtime implicitly.

## Forge package compatibility

The package keeps its own tested SolidCraft compatibility guard. CI must verify
that its declared `SOLIDCRAFT_VERSION` agrees with the package compatibility
contract.

## SCPF CLI identity and error presentation

The CLI exposes the identity of the running SCPF package independently from
SolidCraft runtime compatibility.

Requirements:

- `python -m scpf --version` succeeds without a model path, SolidCraft
  connection or native CLI;
- the reported SCPF version comes from the installed/running Python package
  metadata and must not be confused with `TESTED_SOLIDCRAFT_VERSION`;
- normal model/build/compiler failures are caught at the CLI boundary and shown
  as a short engineering-level error;
- concise output includes SCPF version, the primary exception message and the
  model/source filename + line number when traceback/source information makes
  that location available;
- concise output points to `--debug` for a full traceback;
- `--debug` preserves the original exception traceback and additionally
  reports the exact Forge Git revision when the running package is inside a
  reliably discoverable Git checkout;
- unexpected internal exceptions may be labelled as internal failures, but the
  full traceback is still hidden by default;
- library APIs such as `run_script()` continue raising their original
  exception types; this requirement changes CLI presentation only.

## Verification package dependency

Library ownership and runtime packaging are separate concerns.

The released CAD runtime images must not embed `lib.py.cad.verification`.
Forge supplies the exact released verification package through the CAD-CI
dependency graph.

Requirements:

- one `cad-verification-package` item prepares exactly one wheel from the
  pinned released verification source;
- the wheel is built/prepared once per selected graph, not once per model;
- model verification depends on both `forge-package` and
  `cad-verification-package`;
- reference verification depends on `cad-verification-package`;
- both runtime containers mount the dependency wheel read-only and add it to
  `PYTHONPATH`;
- changing the verification-library pin must not require a Docker runtime
  release;
- changing model-local `verification/verify.py` must not require either a
  package or runtime release;
- Forge owns only the dependency pin and transport, never verification-library
  implementation.

## Declarative model verification

A migrated Forge model owns only model-specific verification data.

For SolidCraft-backed model verification:

- the model may define a `SolidCraftVerification` value in
  `verification/verify.py`;
- body counts, expected bounds, parameter values, timeline expectations,
  mutation command paths and other model-specific expected values remain with
  the model;
- `verify.py` contains data only and must not contain checker callbacks;
- the model must not parse SolidCraft result JSON, invoke SolidCraft
  verification commands, construct verification checks or write
  `verification.json`.

The shared Forge launcher owns only the producer boundary required before
verification:

1. build/locate the exact Forge wheel;
2. locate the exact released verification dependency wheel;
3. compile/replay the Forge model into the initial native SolidCraft `.sc`
   model;
4. load the model-local `verification/verify.py`;
5. call released `run_solidcraft_verification()`.

Shared SolidCraft evaluation, mutation, inspection, schema interpretation,
comparison and report construction are responsibilities of released
`lib.py.cad.verification`.

Model migrations are proven in reviewable batches after the representative
simple-box proof.


## Staged model participation

Forge may declare released CAD-CI item participation with the generic
`process` field.

- Forge does not parse, plan or execute `process` semantics itself.
- `tool.cad.ci` / `lib.py.cad.ci` remain the sole owners of those semantics.
- `scpf` tool/library build and tests must remain processed during staged model
  verification.
- A staged proof may explicitly mark selected model verification items
  `process: true` and other model verification items `process: false`.
- Shared/reference items remain processed where the current dependency graph
  requires them.
- Changing staged participation must not alter model verification ownership or
  verification-library boundaries.


## Forge package CI dependency boundary

Forge package creation, Forge unit tests and Forge release verification are
separate CAD-CI items.

- `forge-package` builds the SCPF wheel exactly once and publishes `dist/`
  as its item output.
- `forge-tests` depends on `forge-package`, installs that exact dependency
  wheel and runs the reusable Forge unit suite.
- `forge-release` depends on `forge-package`, uses that exact dependency
  wheel and runs the fixed release-verification example set.
- release-candidate identity inputs, including `CHANGELOG.md`, must invalidate
  `forge-release` so the durable release-verification evidence is produced
  from the exact candidate SHA rather than reused from an older source commit.
- model verification items depend on `forge-package` and
  `cad-verification-package` only.

A model verification must not require `forge-tests` or `forge-release` to
complete before its own model check can execute.

The test and release-verification items must watch Forge package source as well
as their own test/example sources so a package implementation change still
selects both checks.

The package wheel must not be rebuilt independently by tests, release
verification or model items. All consumers use the output root supplied by the
generic CAD-CI dependency context.

This split changes dependency ownership only. It does not add Forge-local
selection, scheduling, caching or parallel-execution policy.

## CI reliability during staged verification

Forge CI must run only against an exact externally accepted `tool.cad.ci` /
`lib.py.cad.ci` release pair.

During the current staged five-model proof:

- exactly `simple-box`, `anchor-topology-mutation`, `attach-angle`,
  `four-corner-l` and `xz-anchor` have model verification enabled;
- every other historical model item remains explicit `process: false`;
- independent reference items remain separately selected by normal released
  CAD-CI changed-path/dependency semantics;
- Forge must not add a second planner or consumer-side changed-path engine to
  enforce this staging.

Structured CAD-CI evidence is authoritative for what executed.

For every selected item/step that runs, the current CAD-CI evidence under the
item's `.cad-ci` namespace must be sufficient to determine:

- item and step identity;
- execution outcome;
- whether the consumer action executed;
- run start/finish;
- action start/finish and duration when an action executed.

Console text is diagnostic only and must not be the sole source used to decide
what CI actually executed.

The staged proof is considered reliable only when representative active-model
changes can be explained from:

1. the repository configuration;
2. the released CAD-CI selected graph;
3. the resulting structured item/step evidence.

For #484, performance interpretation must additionally separate immutable
SolidCraft image acquisition from subsequent container/process/model work.

The Forge-owned model launcher may emit diagnostic duration lines for:

- Forge command compilation;
- immutable image pull;
- Docker container creation/start to the container entry shell;
- Python interpreter/module bootstrap from container entry to the Forge runtime
  function;
- total container/process execution;
- in-runtime verification-library import;
- native model production;
- released SolidCraft verification;
- total in-runtime work.

These durations are diagnostics only. They must not affect selection, execution,
pass/fail decisions or structured CAD-CI evidence. Verification semantics must
not be weakened to improve timing.

## Standalone Sketch extrusion Boolean operands

A standalone `Sketch(...).extrude(...)` is a solid-producing native feature and
must be composable as a Boolean operand without first attaching the Sketch to
the target body.

Requirements:

- `body + sketch.extrude(...)` lowers the standalone native
  `solid.extrude` with `operation=join` and the existing body as its target;
- `body - sketch.extrude(...)` lowers it with `operation=cut`;
- `body & sketch.extrude(...)` lowers it with `operation=intersect`;
- standalone `RoundedRectangle2D` uses the same native rounded-rectangle profile lowering as an attached Sketch;
- the Sketch keeps its authored plane, plane offset, profiles, profile picks,
  exact-region selection, signed/symmetric extrusion direction and editable
  parameter expressions;
- Boolean lowering must not create a temporary second body and then combine it;
  use SolidCraft's native extrusion operation/target contract directly;
- root standalone Sketch extrusion remains `operation=new` / `body_name`;
- attached `Sketch(on=...)` extrusion keeps its existing
  `explicit_sketch_extrusion` lowering;
- primitive-only CSG remains on the primitive CSG compiler.

SolidCraft 0.45 explicitly supports `new|join|cut|intersect|auto` on
`solid.extrude.operation`; Forge only exposes the deterministic operations
required by the public Boolean operators.

## Model command-contract coverage

The staged model-verification path preserves the former Q1/Q2 ownership split
without retaining the old qualification runner.

- Q1 is reusable Forge API/compiler evidence and is covered by the normal
  `forge-tests` unit suite.
- Q2 is model-owned command-contract evidence under
  `examples/<model>/tests/`.
- Every processed declarative model verification item must run its own
  command-contract tests against the exact `forge-package` wheel before
  native SolidCraft replay.
- A Q2 failure fails that model item before native verification starts.
- `verification/verify.py` remains data-only and does not contain Q1/Q2 test
  code.
- The fixed `forge-release` example set is release verification and is not a
  substitute for Q2 coverage of every processed model item.
- A processed model item's CAD-CI watch/step inputs must include its
  `examples/<model>/tests/**` files so changing the contract test invalidates
  and reruns that model verification.

This restores command-contract coverage without reintroducing the historical
qualification orchestration.

## Durable generated build output and development lanes

Forge uses the exact externally accepted `tool.cad.ci 0.18.0` /
`lib.py.cad.ci 0.10.0` stack for all selection, execution, durable-scope and
generated-branch mechanics.

Forge explicitly requests `jobs=2` from the released tool on both pull-request
and long-lived branch integration runs. The tool/library/SCons stack remains the
sole owner of target parallelism and scheduling. Forge must not add a local
worker pool, target loop or second dependency scheduler.

The source branches have fixed roles:

- `main` is stable integration;
- `dev-cad` is the long-lived Forge/CAD/product integration lane;
- `dev-ci` is the long-lived Forge CI/infrastructure integration lane.

Normal pull requests are verification-only.

Requirements:

- a pull-request job keeps one stable required-check identity;
- before bootstrapping CAD-CI, a normal PR into `dev-cad` or `dev-ci` may
  cheaply classify the changed filenames;
- if every changed path is below `docs/`, that same required check may finish
  successfully without checking out/installing the CAD-CI tool stack, logging
  in to GHCR or running any site/CAD target;
- any non-`docs/` path must use the normal changed-path-selected CAD-CI
  execution;
- promotion PRs targeting `main` must never use the docs-only shortcut and
  still require complete validation even when their diff is documentation-only;
- a pull request must not publish `build/pr/*`, Pages previews or any other
  durable generated state;
- pull requests do not require `contents: write`;
- PR close events do not need generated-scope cleanup because PR scopes are no
  longer created;
- Forge must not reimplement generic selection to achieve this.

Durable publication occurs only for an integration event on one of the three
long-lived source branches. Normal source updates arrive through `push`; a
policy-controlled merge may explicitly invoke the same integration path through
`workflow_dispatch` because GitHub suppresses recursive push workflows created
with `GITHUB_TOKEN`.

The generated `build` branch contains complete reconciled scopes:

```text
main/
dev-cad/
dev-ci/
```

For each push:

- `main` uses the released complete-main update/publication path;
- `dev-cad` uses released named-scope update/publication with name
  `dev-cad`;
- `dev-ci` uses released named-scope update/publication with name
  `dev-ci`;
- main selection uses the normal push base/head and current repository membership;
- an existing named dev scope uses its own durable
  `build/<lane>/build.json.source_commit` as the incremental base; do not
  rely on `github.event.before`, because branch-create events use an all-zero
  before SHA;
- deletion-only updates remain valid;
- a first publication for a missing named scope is bootstrapped from one
  complete processed run and `build prepare-named`;
- updating one scope must preserve both unrelated complete scopes;
- Forge must not inspect or merge generated branch trees itself.

The same runner that executes CAD-CI continues through build preparation,
publication and Forge-owned site generation. There is no Actions artifact
handoff and no second tool/library bootstrap.

For long-lived branch integration, Forge must use the released tool.cad.ci
0.18.0 root composite action in durable mode. That action owns generic durable
scope discovery, incremental-base resolution, the single CAD-CI/SCons run,
complete build-scope preparation and durable build publication.

Forge workflow YAML must not duplicate those generic phases locally. Forge
retains only repository policy (supported source lanes and PR docs-only/full
promotion policy), Forge-owned site generation, and the final generic Pages
publication call that publishes the already-built site content.

## Lane Pages publication

The generated `gh-pages` branch remains one shared publication branch.

Its layout is:

```text
/                 stable main site
/dev-cad/         dev-cad integration preview
/dev-ci/          dev-ci integration preview
```

Requirements:

- `main` publishes the stable root and explicitly preserves both named dev
  subtrees;
- `dev-cad` replaces only the `dev-cad` subtree;
- `dev-ci` replaces only the `dev-ci` subtree;
- one lane may never remove or overwrite another lane's site;
- the stable root must never be sourced from a development build scope;
- the public GitHub Pages source switch tracked by #366 remains a separate
  operational decision and is not performed by #572.

Forge site generation must consume the exact complete scope prepared on the
same runner and record that actual scope in provenance and Verification
metadata. Main output records `main`; development output records its named
scope.

## Lane concurrency, promotion and merge policy

Each long-lived source branch owns an independent concurrency group. A newer
`dev-cad` run may cancel an older `dev-cad` run but must not cancel
`dev-ci` or `main`.

Short-lived feature/fix branches target one dev lane and are squash-merged.

Promotion is direct from the accepted long-lived lane:

```text
dev-cad -> main
dev-ci  -> main
```

Promotion PRs require complete validation.

Merge method selection must be machine-controlled:

- base `main` + head exactly `dev-cad` or `dev-ci` -> normal merge commit;
- every other PR -> squash merge.

Repository automation must use the policy-controlled merge workflow rather than
calling the merge API with a chosen method.

The policy workflow must reject draft, unmergeable or non-green PR heads. After
a successful merge into a durable source ref (`main`, `dev-cad` or
`dev-ci`) it must explicitly dispatch the Forge integration workflow on that
ref, because merges performed with the repository `GITHUB_TOKEN` do not
generate a second workflow run from their resulting push event.

After a direct lane promotion it must ensure that the promoted long-lived lane
exists and points at the resulting main merge commit, including while repository
`delete_branch_on_merge` is still enabled, and dispatch Forge integration for
both `main` and the restored promoted lane.

Merged source-branch cleanup is allow-list based. Only explicitly temporary
prefixes may be deleted automatically. `main`, `dev-cad`, `dev-ci`,
generated branches and backup refs are never cleanup targets.

After promotion the other dev lane incorporates main separately; unpromoted
work in that lane must never be overwritten.

Generic source-freshness, complete-scope reconciliation and generated-branch
retry behavior remain CAD-CI responsibilities.

## Isolated reference items

Independent reference implementations for an active model are CAD-CI items in
their own source directories.

For a migrated model:

```text
examples/<model>/
  verification/reference_geometry.json
  build123d/
    ci.yml
    model.py
  cadquery/
    ci.yml
    model.py
  pythonscad/
    ci.yml
    model.py
  pybosl2/
    ci.yml
    model.py
```

Requirements:

- each reference implementation is independently selectable from Git changes;
- the directory containing the child `ci.yml` is its item root;
- child configuration uses released item-root and parent-relative path
  semantics; it must not repeat the full model repository path;
- a child source change selects that child only unless an explicit shared input
  also changed;
- the model-local `verification/reference_geometry.json` is a shared input of
  all four reference children, so changing it selects all four;
- reference children do not depend on the Forge model item merely to inherit
  selection state;
- model-specific geometry expectations remain only in the model-local contract;
- shared Forge scripts may derive model/reference identity from generic
  `CAD_CI_ITEM_PATH` context, but must not contain a model-name registry;
- released `lib.py.cad.verification` remains the owner of generic geometry
  validation behavior.

During staged migration, a temporary aggregate reference item may cover active
models whose references have not yet been split. That aggregate:

- must exclude every model already migrated to isolated reference children;
- must not process `process: false` model references;
- is transitional and is removed when the active proof set is fully migrated;
- must not cause a child-only change in a migrated model to trigger
  all-catalog reference verification.

Forge must not add a second Git-diff selector or cache/fingerprint mechanism.
The exact released CAD-CI planner owns affected-item selection.


## Visual model verification

Forge visual verification separates model/engine policy from generic image
mechanics.

Forge owns:

- which views a model requires;
- conversion from measured SolidCraft body bounds to the deterministic
  SolidCraft snapshot camera;
- the `solidcraft-cli snapshot` invocation;
- approved model-local baseline images or approved encoded baseline payloads;
- model-local expected geometry;
- the fact that visual verification is required for that model.

Released `lib.py.cad.verification` owns:

- normalization and image comparison;
- visual-regression metrics and diff creation;
- orthographic projection and expected box/hole/slot drawing;
- goal and overlay generation;
- one-view `VisualViewEvidence`;
- generic semantic result composition.

Every active Verification model stores visual policy below its own verification directory:

```text
examples/<model>/verification/
  visual.json
  baselines/
    <view>.png | <view>.json
```

All active Verification models require visual verification. A missing
`visual.json` or missing approved baseline for a required view is incomplete
verification, not `not-required`.

The required-view set preserves the historical contract. The default remains
front/right/iso, with model-local overrides where top or another orthographic
view is required to expose holes, slots, patterns or sheet geometry.

`visual.json` contains data only. It must not contain Python callbacks or a
second implementation of generic image/projection logic.

An approved encoded baseline payload may use the released verification-library
baseline schema (`encoding`, `width`, `height`, `data`) plus provenance fields.
Forge must delegate payload decoding to released `decode_baseline()`; it must
not copy base64/zlib/image decoding logic. A migrated historical payload is
preserved byte-for-byte in its encoded `data` field.

The historical render contract remains:

- SolidCraft snapshot: 720 x 540;
- normalized regression: 96 x 72;
- changed-pixel threshold: 12;
- maximum mean absolute difference: 6.0;
- maximum changed-pixel fraction: 0.08.

Approved baselines are versioned model data. A CI render must never replace or
approve its own baseline.

Approved historical baseline pixels may be migrated into model-local encoded
baseline payloads without pixel re-encoding or reapproval. The migration must
retain the exact decoded compressed/image baseline bytes plus source/approval
provenance. Non-canonical base64 text padding may be normalized when needed by
the released decoder, provided the decoded bytes remain identical and the
normalization is recorded in model-local provenance.

The removed central historical baseline manifest is migration evidence only and
must not become a runtime registry.

For each required view, normal model verification retains:

- actual PNG;
- SolidCraft camera JSON;
- regression diff PNG when a baseline exists;
- independent expected-shape goal PNG;
- overlay PNG;
- structured view evidence with pass/fail/missing state.

The visual stage reuses the baseline measurements already produced by
`run_solidcraft_verification()`. It must not reevaluate the native model only
to derive camera bounds.

The historical projection convention remains:

- front view: X right, Z up;
- top view: X right, Y up.

SolidCraft and the verification library share yaw direction. The equivalent
verification-library orthographic camera uses the negated SolidCraft pitch and
a half-height distance equal to `0.4 * SolidCraft distance`.


## Versioned verification diagrams

Forge retains the historical CADCraft verification/documentation diagrams as
versioned source evidence.

Requirements:

- diagram sources live below `verification/diagrams/sources/`;
- the required source set contains the historical joint/corner-bracket diagrams;
- every source declares the exact supported CADCraft version;
- the diagram result remains a separate CAD-CI item and must not execute Forge
  or SolidCraft models;
- CADCraft is supplied by the immutable released `cad-reference` runtime;
- Forge must not download, cache, checksum or install the CADCraft executable;
- diagram rendering shares the heavy reference container with independent
  reference CAD when the reference batch is active;
- each source renders a non-empty SVG and DXF;
- the item output retains the original source JSON, rendered artifacts and one
  provenance manifest containing tool version, archive checksum and artifact
  hashes;
- source/tool pin changes invalidate the diagram item through normal CAD-CI
  inputs;
- normal model changes do not select the diagram item.

Forge owns these diagram sources and CADCraft command invocation. The CADCraft
binary/version/archive lifecycle belongs to `docker.cad.solidcraft`. This work
does not belong in lib.py.cad.verification because it is
documentation/evidence generation, not generic model comparison.


## Semantic verification summary

F11 restores the semantic qualification result already used by the public
Qualification pages. It must not introduce a new public report vocabulary or a
new sixth visible qualification level.

For each case the public semantic checks remain:

- `integration`;
- `native_model`;
- `geometry`;
- `saved_design`;
- `visual`.

This is the existing schema-5 `qualification-result.json` meaning. The current
Pages presentation and status labels remain the compatibility target.

Independent PythonSCAD, pyBOSL2, CadQuery and build123d results remain separate
reference evidence. Their presence and success are qualification prerequisites,
but F11 must not add a new visible `reference` row to the public case status
summary merely because storage/CI is being migrated.

Forge composes the result only from already-produced CAD-CI, model-verification,
visual and reference evidence. The summary layer must not compile Forge models,
start SolidCraft, execute reference CAD, render/compare images, mutate designs,
or implement a second CAD-CI selector.

Released `lib.py.cad.verification` owns generic semantic status precedence and
composition. Forge owns only the mapping from Forge evidence to the existing
qualification fields.

`saved_design` is `not-required` when no saved-design check exists.

For every active Verification model, `visual` is required and must be
composed from the current durable `model_verify/visual.json` evidence.
A missing visual report, missing required view or missing approved baseline is
incomplete/failing verification according to the existing semantic precedence;
it must never be converted to `not-required`.

A presentation preview is never evidence for a visual PASS and may not replace
the required visual-verification evidence.

Independent-reference summary input is read only from the canonical
`examples/<slug>/<implementation>/` child items. Batch producer copies are not
additional public/reference summary inputs.

Missing/failed/error/review/blocked evidence must remain distinguishable.
Evidence references must be preserved.

The original staged F11 proof used five cases. Stable Pages now applies the
same adapter semantics to the complete active catalog using the resolved
durable evidence tree.

F11 code operates on a resolved evidence tree and is independent from producer
execution. Wiring a durable resolved tree into the collector belongs to
#366/#497, so F11 must not create a cold CAD-CI fan-in that rebuilds every
producer.


## Verification runtime batching

Logical verification items remain independently selectable and retain their own
durable output/evidence paths. Expensive CAD runtimes are not required to match
those logical item boundaries.

Forge verification therefore batches expensive runtime work:

- one SolidCraft runtime processes the current declarative model list;
- one reference runtime processes the current independent-reference list;
- build123d uses one isolated interpreter/import for its complete case list;
- CadQuery, PythonSCAD and pyBOSL2 process their complete lists in the shared
  reference process;
- CADCraft processes the complete diagram source list inside the same heavy
  reference runtime batch.

Per-case verification state remains isolated. Each model/reference has its own
input, output directory and structured result. A failure in one case must not
prevent later cases in the same batch from running. After the complete list is
processed, the batch returns failure when one or more cases failed.

CAD-CI continues to own logical selection, dependencies, SCons state, caching
and durable publication. Forge owns only the batch runtime invocation and the
mapping from batch results back to existing per-case outputs. No generic worker
pool or batch scheduler is added to lib.py.cad.ci.


## Example documentation preservation

The #548 migration is a source relocation, not a rewrite.

The last canonical pre-removal case documentation from
`qualification/cases.py` must be preserved verbatim per owning example. The
migration may change headings/formatting and file location, but it must not
summarize, reinterpret or silently omit the existing engineering statements.

The last canonical per-case geometry sufficiency rationale from
`qualification/geometry_contracts.py` must also be preserved verbatim. In
particular, the explanation of why outer bounds are or are not sufficient is
human engineering documentation, not a value to reconstruct later from machine
checks.

`model.yml` keeps only the agreed generic page metadata fields:
`section`, `priority`, `title`, `tagline`, `description`, `parameters`, and
`stages`. It is not a second verification contract.

Machine expectations, tolerances and saved-design checks remain solely in
`verification/verify.py`.

## Example-owned presentation metadata

Every current Forge verification example is self-describing for generated
documentation.

`examples/<slug>/model.yml` is the authoritative source for human-facing
example metadata. The required schema contains:

- `section`;
- positive integer `priority`;
- `title`;
- `tagline`;
- `description`;
- `parameters`;
- non-empty `stages`.

Verification explanation and historical engineering rationale live in the
example documentation, not in additional `model.yml` verification fields.

These fields describe the example for navigation/presentation. `priority` is presentation-only and controls ordering within the example's section; lower values render first. These fields must not become a second machine verification contract. Exact expected geometry, parameters, tolerances and saved-design
expectations remain in `verification/verify.py`.

Generated Pages obtain actual status, measurements and evidence links from the
accepted durable `build/main` item output. `model.yml` must never claim a
current PASS/FAIL result.

The site generator discovers examples from the filesystem and their local
metadata. It must not maintain a central model-name/page-content registry.

## Site source separation

HTML generation must be structurally separated from site data/orchestration.

- complete page layout belongs in external templates;
- reusable dynamic fragments should normally use external templates;
- when Python-generated markup is justified, it must live only in an explicitly
  named HTML-rendering module rather than in `site/build.py`, loaders or
  evidence code;
- prose-heavy guide content belongs in external Markdown or template content;
- CSS and browser JavaScript belong in static files;
- generated API facts continue to come from the public implementation/docstrings;
- example page metadata comes from local `model.yml`;
- preserved engineering explanation comes from local `README.md`;
- executable model facts come from source/verification files and durable evidence.

Source/evidence/orchestration modules may load, validate and normalize data,
construct view-models and write generated output. They must not mix that work
with page markup. HTML belongs to templates or to the dedicated HTML-rendering
module; guide chapters and model-specific SVG galleries remain external data.

The current site must not depend on retired `qualification.*` source modules.
The 32 current `examples/` directories and durable `build/main` are the
catalog/evidence sources.


### Presentation metadata selection boundary

`model.yml` is presentation/documentation metadata. Changing only
`examples/<slug>/model.yml` must not select or invalidate model compilation,
SolidCraft verification or independent CAD reference verification.

The lightweight site-source item owns `model.yml` and `README.md` validation
and generated documentation checks. CAD verification inputs are the model source,
verification contract, model-specific command/test data and shared runtime
helpers only.


## Stable Pages durable evidence contract

Stable Pages combines current source documentation with the accepted generic
`build/main` baseline. The stable site is never a source of verification
truth itself.

- canonical model evidence is read from
  `build/main/examples/<slug>/`;
- canonical independent reference evidence is read from the corresponding
  `build/main/examples/<slug>/<implementation>/` child item;
- batch producer outputs under `build/main/ci/*-batch/` are implementation
  detail, not a second public evidence namespace;
- `build/main/build.json` is authoritative for item membership and per-item
  source provenance;
- unchanged accepted items may have an older `source_commit` than the site
  source commit;
- root site `provenance.json` records both the site source commit and the
  immutable build-branch commit used for generation;
- current status/measurements/results shown by Pages must come from durable
  evidence, not from `model.yml`, README prose or historical Pages output;
- preserved human engineering text remains sourced from the local README and
  must not be regenerated from verification JSON.

The cut-over is a content migration, not a content reduction. The stable site
must retain or replace with equivalent current data the existing useful
example, native, reference, saved-design, visual, diagram and raw-evidence
information categories.

### Durable presentation previews

Every accepted model and independent reference item used by stable Pages must
provide one current deterministic ISO presentation image at:

```text
presentation/preview-iso.png
```

This artifact has presentation semantics only.

- it is derived from the accepted native model or the already-verified
  reference STL belonging to that item;
- it does not create a new verification check or status;
- its presence must never be rendered as `visual=PASS`;
- a model that already produced the current ISO visual-verification render
  reuses that render rather than taking a duplicate snapshot;
- a model without visual-verification policy receives one deterministic
  720×540 SolidCraft ISO snapshot from its accepted model and baseline measurements;
- reference items receive one deterministic ISO render of their verified STL;
- CAD rendering, view choice and camera policy remain Forge-owned consumer
  behavior, consistent with the released CAD verification library boundary;
- historical backup renders may be used only as migration references and must
  never be labelled as current evidence.

Keeping previews in accepted item output allows presentation-only site changes
to reuse current CAD evidence without rerunning model/reference verification.

### Stable Pages publication

Forge owns complete site generation and content. Released CAD-CI owns generated
branch publication.

The stable site is published only as one complete directory through
`cad-ci publish pages`. Forge must not reimplement Pages Git fetch, merge,
retry, race or push mechanics. #497 changes only the stable root; PR preview and
preview cleanup lifecycle remains outside this cut-over.


## Public verification Pages

The current public concept is **verification**, not qualification.

- navigation, headings, page titles and stable public URLs must use
  `Verification` / `verification/`;
- retired `Qualification` terminology may remain only in historical material or
  temporary internal implementation names during migration; it must not be
  presented as the current user-facing architecture;
- every verified model page must show the complete Forge Python model source
  inline;
- every available independent reference implementation (PythonSCAD, pyBOSL2,
  CadQuery and build123d) must show its complete Python source inline beside
  that implementation's current preview/result evidence;
- reference source visibility is source-owned and must not depend on durable evidence availability; source-only builds still show all four reference sources, while stable builds add current durable result evidence beside them;
- source links are supplementary; replacing inline source with links is a
  content regression;
- displayed source must come from the owning example source tree, while
  PASS/FAIL, measurements and generated CAD artifacts continue to come from the
  accepted durable build evidence;
- the verification index must group examples by the existing `section` field in
  each example's `model.yml`;
- grouping order must be deterministic, and no second central catalog of group
  membership may be introduced;
- each example declares a local integer `priority` in its `model.yml`; examples
  inside one section are sorted by that priority and then slug as a deterministic
  tie-breaker;
- section presentation configuration uses `priority`, not positional `order`;
- public section label/priority translation is presentation configuration under
  `site/content/verification-sections.yml`, not Python source;
- the six existing section slugs keep the preserved public labels and order:
  `fundamentals` → `1 · Basic geometry`, `features` →
  `2 · Parent/child features and faces`, `parameters` →
  `3 · Parameters and dependencies`, `components` →
  `4 · Components and occurrences`, `anchors` → `5 · Anchors and local frames`,
  and `associativity` → `6 · Associative relationships`.


## Verification cut-over compatibility

The canonical public terminology and route are `Verification` and
`/verification/`.

The stable site must also preserve the pre-cut-over public
`/qualification/` URLs as compatibility aliases:

- the old root redirects to `/verification/`;
- old case paths redirect to the corresponding current Verification case;
- `coverage/`, `results/` and `joint-anatomy/` redirect to current
  canonical special pages;
- the old `qualification/manifest.json` path serves the exact same current
  manifest bytes as `verification/manifest.json`;
- the six historical joint-anatomy CadCraft JSON paths remain available.

Compatibility output must not reintroduce Qualification as current navigation or
as a second authored content tree.

The canonical Verification site must preserve the standalone knowledge that
existed before cut-over:

- a current durable results table derived from normalized build/main evidence;
- a capability/API coverage page derived from source-owned coverage
  declarations and linked current Verification cases;
- the authored joint-origin/corner-bracket anatomy explanation, backed by the
  current six source-owned CadCraft plans and durable rendered diagrams.

Human explanatory copy belongs in templates/content. Python may validate,
compose rows, resolve evidence URLs and write compatibility aliases.

## SolidCraft 0.45 parametric native Slots

Forge preserves SolidCraft's native Slot history and the exact 0.45 command
contracts captured under `docs/reference/solidcraft/0.45.0/`.

Requirements:

- all five native `Slot*2D` constructors accept a fixed positive width or a
  Forge `Parameter` / `Expression`;
- current evaluated width must remain positive and finite;
- a fixed-point Slot lowers directly to its native `sketch.slot.*` creator,
  including a symbolic width expression where SolidCraft accepts it;
- direct SolidCraft Slot point fields remain numeric `PlainPoint` values;
- the three straight Slot constructors may accept symbolic authored point
  coordinates only when the current axis is horizontal or vertical;
- symbolic straight endpoints lower to numeric seed points plus native
  `sketch.draw.dimensioned` dimensions;
- the dimensioned creator uses the canonical 0.45 roles `length` and
  `width`;
- Forge constrains the returned native `centre_line` horizontal/vertical and
  drives the returned native `middle` point from the sketch origin so authored
  position remains parameter-driven;
- saved-design position mutation is qualified while the driven middle point
  remains on its authored side of each sketch-origin axis; crossing an origin
  axis is not supported in this release because SolidCraft 0.45 linear
  dimensions are unsigned distances and the numeric seed owns the side;
- the two perpendicular endpoint coordinate intents must be identical so a
  horizontal/vertical Slot cannot become skewed after parameter mutation;
- diagonal straight Slots remain supported only when their authored points are
  fixed numeric coordinates;
- arc-Slot authored points remain fixed numeric coordinates in this slice;
- no rounded-rectangle fallback, numeric baking or Forge-owned sketch solver is
  allowed;
- qualification must prove generated commands, native 0.45 acceptance and
  saved-design parameter mutation/rebuild.


## Shared-batch dependency-output projection

Forge consumes only an exact externally accepted CAD-CI release pair for
dependency-output projection.

For model/reference shared batches:

- expensive CAD/runtime work remains one Forge-owned shared producer action;
- the producer writes each child result in the exact output shape owned by that
  child item below an `items/<repository item path>/` projection root;
- model projection roots contain `solidcraft.json` and `model_verify/`;
- reference projection roots contain `references/`, including the child-scoped
  `verification.json` report and the implementation result tree;
- the shared diagram result remains `diagrams/`;
- child model/reference/diagram items use released CAD-CI `copy:` actions;
- child projection steps must not launch Forge materializer processes;
- child copy actions must not materialize the complete dependency output;
- real model-owned `contract_test` commands remain separate executable steps;
- Forge does not implement bundle selection, projection, signatures, caching,
  CURRENT decisions or jobs scheduling.

The exact accepted dependency for this capability is tool.cad.ci 0.18.0 backed
by lib.py.cad.ci 0.10.0. A future pin change requires the normal external
released-stack acceptance chain before Forge adoption.

Performance evidence is diagnostic, not an SLA. #261 must compare the
promotion-equivalent jobs=2 post-batch tail before and after migration, and must
not increase jobs beyond 2 merely to hide projection overhead.


## Connected mixed-curve Sketch profiles

Forge supports one authored closed Sketch profile made from connected straight
line and circular-arc segments without approximating arcs as polygon edges.

Public authoring contract:

```python
with Sketch(name="Blank", plane="XY") as sketch:
    contour = sketch.profile(start=(0, 0))
    contour.line_to((40, 0))
    contour.arc_through_to((40, 20), through=(50, 10))
    contour.line_to((0, 20))
    contour.line_to((0, 0))
    contour.close()
```

Requirements:

- `Sketch.profile(start=...)` creates one connected-profile builder owned by
  that active Sketch;
- `line_to(end)` authors one straight native segment from the builder's
  current endpoint;
- `arc_through_to(end, through=...)` authors one native three-point circular
  arc from the current endpoint;
- `arc_center_to(end, center=..., clockwise=False)` authors one native
  center-point circular arc from the current endpoint;
- segment point coordinates may contain the same Forge Parameter/Expression
  values accepted by native Sketch point fields and must remain expressions in
  the emitted SolidCraft design;
- each segment's start is the previous segment's authored endpoint; callers do
  not pass raw native curve/point ids or command dictionaries;
- lowering uses SolidCraft `connect=true` so coincident connectivity is native
  and survives parameter edits;
- `close()` validates a closed authored loop and registers exactly one profile
  in the owning Sketch; it must not silently invent a line or arc;
- an unclosed builder is an authoring error when the Sketch scope exits;
- zero-length lines, degenerate arcs and non-finite authored geometry are
  rejected before replay;
- the connected profile is accepted anywhere the existing one-profile
  standalone Sketch contract is accepted, including ordinary
  `Sketch.extrude()` and `Sketch.sheet_metal()`;
- existing Rectangle2D/RoundedRectangle2D/Circle2D/Polygon2D/Slot APIs remain
  unchanged convenience profiles;
- no polygon approximation is permitted for an authored arc;
- no raw SolidCraft dictionaries or generated curve ids become public API.

The initial slice does not expose tangent-arc authoring. SolidCraft 0.45 has a
native tangent-arc command, but that form depends on a previous native curve
reference. Add it only after Forge has a deliberate public entity-reference
contract rather than guessing runtime ids.

Saved-design qualification must prove that editing at least one straight
endpoint dependency and one arc dependency preserves one closed native profile
and one valid resulting body after save/reopen.

## SolidCraft 0.45 sheet flange family

Forge's remaining sheet-metal coverage follows the pinned SolidCraft 0.45
command registry, not the earlier 0.42 mental model.

SolidCraft 0.45 exposes one `sheet.flange` feature family:

- `type=base` creates sheet material from a closed Sketch profile and is already
  consumed by `Sketch.sheet_metal()`;
- `type=edge` creates flange material from selected edge(s) of an existing sheet body;
- `type=contour` creates sheet material from an **open** Sketch curve chain and a distance.

There is no standalone `sheet.contour` command in the current supported registry.

Shared material properties remain rule-owned:

- sheet thickness;
- K-factor;
- default bend radius.

Forge must not expose those again as per-flange material overrides where the
native command refuses them.

The remaining work is deliberately split:

- edge flange is one focused Shape/sheet feature contract;
- open connected curve-chain authoring is a reusable Sketch contract, distinct
  from #567's closed profile builder;
- contour flange consumes that open-chain contract only after it is independently
  qualified.

No child may fall back to extruded/fused solid approximations or caller-authored
raw SolidCraft command dictionaries.


## Native sheet edge flange

Forge exposes the first focused SolidCraft 0.45 edge-flange slice on an
existing Forge sheet body.

Public intent:

```python
sheet = sheet.flange(
    edges=[(40, 0, 2)],
    height=20,
    angle=90,
    height_from="outer",
    position=None,
    flip=False,
)
```

Requirements:

- the operation applies only to an existing native Forge sheet history;
- lowering uses one native `sheet.flange(type="edge")` command;
- `edges` is a non-empty sequence of explicit fixed finite XYZ pick points;
- `height` is a positive length and may remain a Forge Parameter/Expression;
- `angle` is an editable angular value accepted by the native command;
- `height_from` is one of `outer`, `inner` or `tangent`;
- `position` is optional; when supplied it is one of `inside`, `outside`,
  `middle`, `material_outside` or `tangent`; when omitted Forge leaves the
  native SolidCraft default in control;
- `flip` is boolean;
- the existing sheet rule remains authoritative for thickness, K-factor and
  default bend radius; Forge does not duplicate those inputs on the flange API;
- caller-authored SolidCraft edge dictionaries are not public API in this slice;
- per-edge angle/height overrides, segment dictionaries, chained `then`
  bends and corner-relief overrides are out of scope;
- the operation must preserve the existing sheet body/history and must not
  lower through solid extrusion/fusion approximations.

Qualification must prove native edge-flange history, one editable height/angle
saved-design mutation, save/reopen stability and flat-pattern continuity.
