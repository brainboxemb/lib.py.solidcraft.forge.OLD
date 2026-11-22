# Forge repository plan

This file is the current source of truth for unfinished work in
`lib.py.solidcraft.forge`.

Forge has two parallel responsibility areas:

1. the **CAD library itself** — public API, compiler/lowering, modelling
   semantics, examples, native qualification and model-specific verification;
2. the **CI/verification/runtime integration around that library** — generic
   CAD-CI consumption, durable build/Page publication, verification package
   integration, runtime-image consumption and release mechanics.

Neither area is subordinate to the other. `dev-cad` and `dev-ci` are
independent execution lanes and should progress in parallel whenever there is no
real dependency between them.

Permanent requirements, design, API and release contracts belong in the normal
documents under `docs/`. Issues keep implementation detail and history.

## Current accepted baseline

Permanent source lanes:

```text
main
dev-cad
dev-ci
```

### Forge package release

The current released Forge baseline is **v0.11.0**.

- annotated tag: `v0.11.0`;
- tagged source commit:
  `9258d54079981604b6dd777a4c4face897c190fe`;
- GitHub Release:
  `https://github.com/brainboxemb/lib.py.solidcraft.forge/releases/tag/v0.11.0`;
- release-candidate Forge run: `45004129325` — success;
- durable `build/main`, `ci/forge-release`, `ci/release-policy` and stable
  Pages all resolved to that exact source commit before publication.

Source package version `0.11.0` is therefore released state, not release
preparation. New user-visible work belongs under the fresh `[Unreleased]`
changelog section.

### Immutable SolidCraft runtime

- `docker.cad.solidcraft v0.3.4`;
- exact runtime source commit
  `89acce00bd760c523251c6c84d291d758c2a4dc5`;
- `solidcraft-cli 0.45.0`;
- immutable roles `cad-solidcraft:v0.3.4` and
  `cad-reference:v0.3.4`.

### Generic CAD-CI stack consumed by Forge

- `lib.py.cad.ci 0.9.3` @
  `74486c441f1f2b170ff3dc06e0edcaf662fbec6b`;
- `tool.cad.ci 0.17.0` @
  `d88d6e189c12edb5a30158c068145c099c17a019`;
- external jobs=2 acceptance: `tool.cad.ci.test` #66 / PR #67;
- Forge explicitly uses `jobs=2` on PR and durable integration runs.

Performance evidence remains diagnostic rather than an SLA:

- selective startup: 26.507 s -> 1.375 s after the accepted startup work;
- jobs=1 full promotion #636: 4m54s;
- jobs=2 #645: 4m44s first run and 3m12s exact-SHA rerun;
- clean jobs=2 rerun: 7.015 s pre-target, 62.238 s model verification and
  59.616 s reference verification with the heavy batches overlapping.

## Recently completed default-branch work

- #355 / #646 / #651: SolidCraft 0.45 parametric native Slot support accepted
  and promoted through the normal `dev-cad -> main` merge.
- #637 / #645: exact CAD-CI 0.17.0 with explicit jobs=2 accepted and promoted
  through the normal `dev-ci -> main` merge.
- #649 / #650: repository handoff/AGENTS corrected to describe both CAD-library
  and CI/integration responsibilities.
- #642 / #652 / #653: release contract restored, release publication made
  explicit and owner-controlled, exact candidate `forge-release` evidence
  enforced, and Forge **v0.11.0** published from
  `9258d54079981604b6dd777a4c4face897c190fe`.

Publication run `45004182308` created and verified the release successfully but
its final issue-result comment failed because Markdown backticks were evaluated
by Bash command substitution. #654 owns only that reporting fix and this
post-release reconciliation; it must not move or recreate v0.11.0.

## Lane rule

- `dev-cad` owns the Forge CAD library: API/compiler/model semantics,
  references, Verification content and CAD-facing behavior.
- `dev-ci` owns infrastructure around that library: Forge CI integration,
  runtime-consumer wiring, durable build state and publication.
- Generic CAD-CI behavior is fixed and released in its owner repository first.
- Generic verification behavior is fixed and released in
  `lib.py.cad.verification` first.
- Runtime construction/release is fixed in `docker.cad.solidcraft` first.
- A blocked CAD issue remains CAD work; dependency handoffs do not move lanes.

Short-lived feature/fix PRs target one development lane and are squash-merged.
Exact `dev-cad -> main` and `dev-ci -> main` promotions use normal merge
commits through the repository `/merge` policy. Every other PR to `main` is
squash-merged.

## Active workstreams

### WS0 — post-release governance

Primary lane: repository-wide governance.

#654 is **now**:

1. keep the released v0.11.0 tag/Release untouched;
2. update primary docs to the released state;
3. fix only the post-publication result-comment construction;
4. retain regression coverage for the owner-controlled release path;
5. merge through `/merge` and then close #654.

No new CAD/API implementation should be stacked before this reconciliation is
on `main`.

### WS1 — CI performance and integration

Primary lane: `dev-ci`.

#261 is **next** and may proceed independently of the CAD lane after #654:

1. separate immutable-image pull time from container execution across repeated
   promotion-equivalent runs;
2. explain reference-image pull variance;
3. identify the remaining serial SCons tail;
4. fix only the owner layer of the dominant remaining cost;
5. do not increase jobs beyond 2 without new evidence.

If the dominant remaining cost belongs to image distribution/runtime packaging,
the implementation belongs in `docker.cad.solidcraft`, not Forge.

### WS2 — next CAD-library work

Primary lane: `dev-cad`.

After #654, the current priority set is:

1. #354 standalone Sketch extrusion as boolean operand;
2. #567 mixed line/arc closed Sketch profiles;
3. #568 native sheet-metal flange/contour features;
4. #349 focused Revolve child first; broad remaining SOLID › CREATE inventory
   later.

These may be split into independent focused PRs where their native contracts do
not depend on one another.

### WS3 — Verification/reference quality

Primary lane: `dev-cad`.

- #570 remove CADCraft from explanatory Verification diagrams without moving
  generic rendering into Forge — later.
- #335 replace the sheet-fold build123d solid approximation with actual
  build123d sheet-metal semantics — later.

### WS4 — API coverage roadmap

Primary lane: `dev-cad`.

- #347 generalize native pattern seeds beyond Sketch extrusions — later.
- #9 first-class Sketch objects, constraints and face workplanes — later epic;
  refresh before implementation.
- #8 hollow primitive intent — later; reconcile with native pipe/shell/boolean
  histories.

### WS5 — AnchorFrame research and interaction polish

Primary lane: `dev-cad`.

- #325 AnchorFrame root-cause research — later.
- #81 inline rotated-occurrence AnchorFrame references — later.
- #82 Joints-folder visibility policy — later.
- #175 historical HUB75-like diagnostic — probably obsolete; consolidate useful
  evidence into #325/background docs.
- #5 generic anchors/constraints — probably obsolete in its current broad form;
  rewrite only the still-missing constraint/associativity scope and consolidate
  overlap with #9.

Production HUB75 work uses explicit Placement, so WS5 does not preempt current
CAD priorities.

## Next release checkpoint

Do not let another large development wave accumulate without a package-release
decision.

The planned next semantic release checkpoint is **Forge v0.12.0**, after the
first coherent post-v0.11 CAD/CI batch has reached `main`. Before stacking a
second large batch:

1. open a dedicated v0.12.0 release issue;
2. audit `[Unreleased]` against the actual merged public changes;
3. decide explicitly which unfinished CAD/CI work is in or deferred from the
   release;
4. use the same exact-SHA durable-evidence and owner-controlled publication
   contract proven by v0.11.0.

This checkpoint is a planning gate, not permission to bump source metadata or
create a dated v0.12.0 changelog section early.

## Open issue assignment — 2026-11-22

Every currently open issue is classified below.

| Issue | Lane | Disposition | Next action |
| --- | --- | --- | --- |
| #654 Post-v0.11 reconciliation/reporting fix | governance | **now** | Record released baseline, fix safe result comment, regression-test it, merge and close. |
| #261 Full Forge integration runtime | `dev-ci` | **next** | Measure image-pull/runner variance and remaining serial tail on jobs=2; fix the owning layer only. |
| #354 Standalone Sketch extrusion boolean operand | `dev-cad` | **next** | Generalize boolean operand lowering for `sketch_base_extrusion`. |
| #567 Mixed line/arc closed Sketch profiles | `dev-cad` | **next** | Deliver a focused connected-curve profile API from qualified native contracts. |
| #568 Native sheet-metal flange/contour | `dev-cad` | **next** | Qualify immutable v0.3.4 native contracts before exposing APIs. |
| #349 Remaining SOLID › CREATE coverage | `dev-cad` | **next** | Split focused Revolve child for the latch; keep broad inventory later. |
| #335 build123d Sheet Metal reference | `dev-cad` | **later** | Replace solid approximation with current build123d sheet-metal workflow. |
| #347 Patterns accept any applied Shape feature | `dev-cad` | **later** | Base source validation on native history-feature identity. |
| #570 Remove CADCraft from Verification diagrams | `dev-cad` | **later** | Replace explanatory sources without moving generic verification rendering into Forge. |
| #325 AnchorFrame regression root cause | `dev-cad` | **later** | Resume only when AnchorFrame becomes an active dependency. |
| #81 Inline AnchorFrame references for rotated occurrences | `dev-cad` | **later** | Investigate occurrence-local frames when AnchorFrame work resumes. |
| #82 Joints folder visibility | `dev-cad` | **later** | Decide interaction/export policy after higher-impact CAD work. |
| #9 First-class Sketch objects/constraints/workplanes | `dev-cad` | **later** | Refresh epic and deliver focused child slices. |
| #8 Tube/RectTube/OvalTube | `dev-cad` | **later** | Reconcile intent with native pipe/shell/boolean histories. |
| #175 HUB75-like AnchorFrame diagnostic | `dev-cad` | **probably obsolete** | Consolidate useful retained evidence into #325/background docs, then close or rewrite. |
| #5 Generic anchors and parametric constraints | `dev-cad` | **probably obsolete** | Separate already-delivered anchor behavior from remaining constraints and overlap with #9 before any implementation. |

## Immediate execution order

1. [#654] Finish this post-v0.11 reconciliation and safe release-result
   reporting fix.
2. After #654, start #261 on `dev-ci` and #354 on `dev-cad` independently;
   #567/#568/focused #349 may follow as their native/dependency gates allow.
3. Before a second large post-v0.11 batch accumulates, open the planned v0.12.0
   release checkpoint and make an explicit include/defer decision.
4. Rewrite/retire #175 and #5 before treating either as implementation work.
