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
- `dev-ci`: `ac47a97cbd2646f292c01c90f2defb95963e48bf`.

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

### #823 — adopt runtime v0.3.5 / SolidCraft 0.48.1

Status: **now / primary blocker resolution**.

Runtime owner `docker.cad.solidcraft` has released immutable **v0.3.5** at
exact source `cb4295271173ac88deed92627c74456300c0393f`, qualified against
SolidCraft **0.48.1**. Authoritative tag build `45366783017` is green for both
runtime roles and published the GitHub Release.

Pre-release external Forge qualification #821 is complete: temporary PR #822
used runtime-main `:edge` only for evidence and final Forge run
`45366059337` passed. The retained #753
`component-cylinder-occurrence` model verification passed on that candidate.
PR #822 was closed unmerged so no mutable edge pin entered a permanent lane.

Adopt the immutable release now:

- pin both runtime roles to v0.3.5;
- set the tested SolidCraft contract to 0.48.1;
- capture the canonical 0.48.1 command registry from immutable v0.3.5;
- update immutable runtime-consumption/reference tests and provenance;
- retain #753 as the product-blocking regression case;
- require full PR and durable dev-cad acceptance before stable promotion.

### #753 — component-local Cylinder joins across occurrences

Status: **blocked only on #823 immutable runtime adoption**.

CAD #388 is the highest-priority downstream blocker for the five-panel HUB75
assembly: component bodies are placed correctly, but one loose set of native
Cylinder join/tool geometry can remain visible at the component-definition
origin.

PR #754 is merged and the retained fixture is durable-green on dev-cad. Runtime
owner qualification proved SolidCraft 0.48.1 renders the retained geometry as
exactly two occurrence islands with no stale third tool object; external Forge
candidate qualification #821 also passed.

Do not add a product-CAD geometry workaround. Close #753 only after #823 pins
immutable runtime v0.3.5 / SolidCraft 0.48.1 and the durable Forge dev-cad run
passes the retained fixture.

### #779 — native whole-sheet perforation

Status: **now / dev-cad in parallel**.

PR #780 has already been rebuilt on the purpose-aware catalog contract and was
green before the #753 blocker fixture advanced dev-cad. Refresh it only after
#823 is accepted so perforation inherits the qualified v0.3.5 runtime baseline.

Keep the focused native `Shape.perforate()` API/compiler/runtime work, but:

- replace the old regression-only `role.yml` with canonical
  `model.yml` using `purpose: verification` and `section: sheet-metal`;
- keep the case at `examples/sheet-perforate/`;
- add normal user-facing API documentation required by #786: Reference,
  Sheet metal Guide, Cheatsheet and `docs/api.md`;
- preserve native perforation/flat-pattern semantics and do not fabricate
  repeated B-rep holes or external reference equivalents.

### #788 — CAD-CI concurrency measurement

Status: **parallel / performance**.

Measure jobs=2/4/6 on one identical post-#785 representative full graph before
changing Forge concurrency or designing bounded batch sharding. Do not remove
Verification coverage or reintroduce per-model runtime startup.

## Open issue assessment

| Issue | Status | Next action |
| --- | --- | --- |
| #788 Re-benchmark Forge CAD-CI concurrency | **parallel / performance** | Measure jobs=2/4/6 on one identical post-#785 full graph. |
| #823 Adopt runtime v0.3.5 / SolidCraft 0.48.1 | **now / blocker resolution** | Pin immutable v0.3.5, capture 0.48.1 reference evidence and require retained #753 verification. |
| #753 Component-local Cylinder joins | **blocked on #823 adoption only** | Close after immutable v0.3.5 is durable-green in Forge; then unblock CAD #388. |
| #779 Native whole-sheet perforation | **next / CAD** | Refresh PR #780 after #823 so it inherits the qualified v0.3.5 runtime baseline. |
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

1. complete #823 on `dev-cad`: immutable runtime v0.3.5 / SolidCraft 0.48.1,
   canonical 0.48.1 command reference, full PR validation and durable branch
   acceptance;
2. close #753 and update downstream CAD #388 only after that durable acceptance;
3. promote the accepted runtime-adoption batch to `main` and make the Forge
   release decision from the stable main build;
4. refresh #779 / PR #780 on the accepted runtime baseline;
5. keep #788 measurement work independent and #751 lower priority.
