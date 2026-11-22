# Forge repository plan

This file is the current source of truth for unfinished work in
`lib.py.solidcraft.forge`.

Forge has two independent responsibility areas:

1. the CAD library itself — public API, compiler/lowering, modelling semantics,
   examples, native qualification and model-specific Verification;
2. CI/runtime/Verification integration around that library — exact released
   generic CAD-CI consumption, immutable runtime consumption, durable build/Page
   publication and release mechanics.

`dev-cad` and `dev-ci` advance independently unless they share a real owner
release or architecture gate.

## Current accepted baseline

Permanent source lanes:

```text
main
dev-cad
dev-ci
```

Current stable integration commit:

`6ed22a5a6cc803e8e34f995deb6e7c6a2bfff7e4`

That merge contains the accepted standalone Sketch Boolean work from #354.
`build/main` and stable Pages both resolve to that exact commit.

### Forge release

Current package release: **v0.11.0** at
`9258d54079981604b6dd777a4c4face897c190fe`.

New user-visible work remains under `[Unreleased]`. The next planned package
checkpoint remains v0.12.0 after a coherent post-v0.11 CAD/CI batch reaches
main.

### SolidCraft runtime

- docker.cad.solidcraft v0.3.4;
- cad-solidcraft:v0.3.4;
- cad-reference:v0.3.4;
- SolidCraft CLI 0.45.0.

### Accepted generic CAD-CI stack

The previous Forge baseline used tool 0.17.0 / lib 0.9.3.

A new exact released pair is now externally accepted for #261:

- `lib.py.cad.ci 0.10.0` @
  `397fb04005b46de8d433cb18c091b1e73714b877`;
- `tool.cad.ci 0.17.1` @
  `1012e6a539a2fddd8194124844fe208bf16cf4e4`;
- `tool.cad.ci.test` #70 / PR #71;
- complete acceptance run `45006989548` — success;
- direct CLI, reusable workflow, same-runner action and dependency-output
  `copy:` all passed on that exact released pair.

Forge still uses `jobs=2`; no jobs increase is part of #261.

## Lane rule

- `dev-cad`: Forge API/compiler/model/Verification/site-content behavior.
- `dev-ci`: CAD-CI/runtime/publication integration.
- Generic CI behavior is fixed and released in lib.py.cad.ci/tool.cad.ci first.
- Generic Verification behavior is fixed and released in lib.py.cad.verification first.
- Runtime packaging is fixed and released in docker.cad.solidcraft first.

Short-lived branches target one lane and are squash-merged. Exact
`dev-cad -> main` and `dev-ci -> main` promotions use the repository
`/merge` policy and therefore normal merge commits.

## Active workstreams

### WS1 — #261 full Forge integration runtime

Primary lane: `dev-ci`. **Now.**

Measured accepted jobs=2 runs showed:

- model/reference heavy batches finish in roughly 60-81 seconds;
- the remaining SCons tail was roughly 107-176 seconds;
- reference image-pull variation explained only about 10 seconds;
- the tail contained many per-item projection actions after shared batch results
  already existed.

Owner-first generic work is complete and externally accepted. Forge may now
consume the released `copy:` action.

Implementation order:

1. pin tool.cad.ci 0.17.1 in the Forge workflow;
2. make shared model/reference batches produce item-shaped projection roots;
3. replace projection-only model/reference/diagram consumer commands with
   declarative `copy:`;
4. keep real per-model `contract_test` commands unchanged;
5. remove obsolete Forge materialize-only code after the config no longer uses
   it;
6. run promotion-equivalent jobs=2 evidence and compare total post-batch tail;
7. if the remaining tail is still material, measure again before changing any
   other owner layer;
8. do not raise jobs beyond 2 in this change.

Target projection layout:

```text
model-verification-batch/
  items/examples/<model>/
    solidcraft.json
    model_verify/...

reference-verification-batch/
  items/examples/<model>/<implementation>/
    references/
      verification.json
      <model>/<implementation>/...
  diagrams/...
```

Child items use `copy: source: items/{item_path}`. The generic library owns
bundle projection; Forge owns only producer layout and declarative config.

### WS2 — CAD-library next work

Primary lane: `dev-cad`.

1. #567 mixed line/arc closed Sketch profiles;
2. #568 native sheet-metal flange/contour;
3. #349 focused Revolve child first, broader SOLID › CREATE inventory later.

### WS3 — Verification/reference quality

- #570 remove CADCraft from explanatory Verification diagrams — later.
- #335 build123d sheet-metal reference semantics — later.

### WS4 — API coverage roadmap

- #347 generalized pattern seeds — later.
- #9 first-class Sketch/constraints/workplanes — later epic.
- #8 hollow primitive intent — later.

### WS5 — AnchorFrame research / interaction polish

- #325 root-cause research — later.
- #81 rotated occurrence-local AnchorFrame references — later.
- #82 Joints-folder visibility — later.
- #175 probably obsolete; consolidate useful evidence into #325.
- #5 probably obsolete in current broad form; separate remaining constraint
  scope from already-delivered anchor behavior.

## Open issue assignment — 2026-11-22

| Issue | Lane | Disposition | Next action |
| --- | --- | --- | --- |
| #261 Measure/reduce full integration runtime | dev-ci | **now** | Adopt accepted tool 0.17.1/lib 0.10.0 copy projection and remeasure jobs=2. |
| #567 Mixed line/arc closed Sketch profiles | dev-cad | **next** | Focused connected-curve profile API. |
| #568 Native sheet-metal flange/contour | dev-cad | **next** | Qualify immutable runtime contracts first. |
| #349 Remaining SOLID › CREATE coverage | dev-cad | **next** | Split focused Revolve child for latch work. |
| #570 Remove CADCraft from Verification diagrams | dev-cad | **later** | Replace explanatory sources without moving generic rendering into Forge. |
| #335 build123d Sheet Metal reference | dev-cad | **later** | Replace solid approximation with actual sheet-metal workflow. |
| #347 Patterns accept any applied Shape feature | dev-cad | **later** | Generalize seed validation by native feature identity. |
| #325 AnchorFrame regression root cause | dev-cad | **later** | Resume only when it becomes an active dependency. |
| #81 Inline rotated AnchorFrame references | dev-cad | **later** | Investigate occurrence-local frames with #325. |
| #82 Joints folder visibility | dev-cad | **later** | Decide interaction/export policy later. |
| #9 First-class Sketch/constraints/workplanes | dev-cad | **later** | Refresh epic and deliver focused slices. |
| #8 Tube/RectTube/OvalTube | dev-cad | **later** | Reconcile intent with native shell/pipe/boolean histories. |
| #175 HUB75-like AnchorFrame diagnostic | dev-cad | **probably obsolete** | Consolidate useful evidence into #325, then close/rewrite. |
| #5 Generic anchors/parametric constraints | dev-cad | **probably obsolete** | Separate remaining constraint scope from overlap with #9. |

## Next release checkpoint

Before a second large post-v0.11 batch accumulates, open the planned v0.12.0
release issue and explicitly include/defer the merged CAD/CI work. Do not bump
source metadata before that release gate exists.
