# Forge repository plan

This file is the current source of truth for unfinished work in
`lib.py.solidcraft.forge`.

Permanent requirements, design, API and release contracts belong in the normal
documents under `docs/`. Issues keep implementation detail and history.

## Current accepted baseline

Permanent source lanes:

```text
main
dev-cad
dev-ci
```

Use the live branch heads and durable
`build/<lane>/build.json.source_commit` manifests for exact identity. Do not
record one hard-coded global baseline SHA here.

Current immutable CAD runtime:

- `docker.cad.solidcraft v0.3.4`;
- exact runtime source commit
  `89acce00bd760c523251c6c84d291d758c2a4dc5`;
- `solidcraft-cli 0.45.0`;
- immutable roles `cad-solidcraft:v0.3.4` and
  `cad-reference:v0.3.4`.

Current Forge-consumed generic CI stack:

- `lib.py.cad.ci 0.9.3` @
  `74486c441f1f2b170ff3dc06e0edcaf662fbec6b`;
- `tool.cad.ci 0.16.2` @
  `59e4c4d3f377f906b33bb2d1fee808f96c6fb1b9`;
- external black-box acceptance: `tool.cad.ci.test` #62 / PR #63.

Newer externally accepted tool surface available for an explicit consumer
experiment:

- `tool.cad.ci 0.17.0` @
  `d88d6e189c12edb5a30158c068145c099c17a019`;
- same `lib.py.cad.ci 0.9.3`;
- external jobs=2 acceptance: `tool.cad.ci.test` #66 / PR #67;
- public evidence proved real overlapping SCons actions through jobs=2.

Forge selective-startup evidence:

- old tool 0.16.1 / lib 0.9.2 pre-target interval: 26.507 s;
- current tool 0.16.2 / lib 0.9.3 pre-target interval: 1.375 s.

The structural owner-layer contract remains authoritative; timing values are
diagnostic evidence.

## Recently completed default-branch work

- #574 / PR #618: complete Verification Technical test details / Raw test files
  hierarchy. Direct dev-cad promotion #638 put it on main; post-merge durable
  build and Pages publication are green.
- #617 / PR #634: canonical SolidCraft 0.45 reference from immutable runtime
  v0.3.4. The raw registry contains 819 commands, exact-matches runtime output,
  and generated Markdown is lockstep-tested against raw JSON. The hand-authored
  0.43 reference tree is removed.
- #340: closed as superseded by permanent lanes and normal two-parent
  promotions.
- #481: conservative evidence-only branch cleanup completed.

## Lane rule

- `dev-cad` owns Forge API/compiler/model/reference/Verification work.
- `dev-ci` owns Forge CI/infrastructure/runtime-consumer/publication work.
- Generic CAD-CI behavior is fixed and released in its owner repository first.
- Runtime construction/release is fixed in `docker.cad.solidcraft` first.
- A blocked CAD issue remains CAD work; dependency handoffs do not move lanes.

Short-lived feature/fix PRs target one development lane and are squash-merged.

Exact permanent-lane promotions:

```text
dev-cad -> main
dev-ci  -> main
```

use normal merge commits through the repository `/merge` policy. Every other
PR to `main` is squash-merged.

## Active workstreams

### Release milestone — Forge v0.11.0

Owner: main/release integration.

Issue #642 owns the next **real** Forge release.

The latest actual GitHub Release remains `v0.10.0`. Source metadata already
carries `0.11.0`, but that is release preparation only.

Release v0.11.0 is planned after the two current integration tracks settle:

- #355 reaches an accepted/promoted state, or is explicitly deferred from
  0.11.0 with the changelog reflecting that decision;
- #637 resolves the jobs=2 experiment and main is left on the chosen accepted
  CAD-CI configuration.

Before another large CAD/API wave is stacked on main:

1. stabilize main with durable build + stable Pages green;
2. reconcile `[Unreleased]` so only shipped work moves into the dated
   `[0.11.0]` section;
3. run the release-candidate verification against one exact main SHA;
4. create immutable tag `v0.11.0` at that SHA;
5. create the GitHub Release;
6. verify tag and GitHub Release both resolve to the intended SHA;
7. record the released baseline in this plan.

A changelog heading or package version is not a release.

### WS0 — CI performance and integration

Primary lane: `dev-ci`.

1. #637 measure full Forge integration with exact externally accepted
   tool.cad.ci 0.17.0 and explicit `jobs=2`.
2. #261 use that evidence to decide the next performance step on the current
   SCons/runtime architecture.

Rules for #637:

- no Forge-local scheduler, worker pool or target loop;
- runtime stays v0.3.4;
- library stays 0.9.3;
- tool pin changes only to exact released 0.17.0;
- jobs=2 is an explicit Forge consumer value, not a hidden global default;
- compare against full promotion #636 baseline before promoting.

### WS1 — active CAD blockers

Primary lane: `dev-cad`.

1. #355 qualify and expose SolidCraft 0.45 parametric native Slot dimensions.
2. #354 standalone Sketch extrusion as boolean operand.
3. #567 mixed line/arc closed Sketch profiles.
4. #568 native sheet-metal flange/contour features.
5. #349 focused Revolve child first; remaining SOLID › CREATE inventory later.

#355 now has an accepted 0.45 evidence baseline. Direct authored Slot point
fields remain numeric; symbolic width is natively supported; straight-Slot
length/position must be qualified through native dimension/constraint mechanisms
rather than expression-valued point fields.

### WS2 — Verification/reference quality

Primary lane: `dev-cad`.

- #570 remove CADCraft from explanatory Verification diagrams without moving
  generic rendering into Forge.
- #335 update the sheet-fold independent build123d reference.

### WS3 — API coverage roadmap

Primary lane: `dev-cad`.

- #347 generalize native pattern seeds beyond Sketch extrusions — P2.
- #9 first-class Sketch objects, constraints and face workplanes — P2 epic.
- #8 hollow primitive intent — P3; reconcile with native pipe/shell histories.

### WS4 — AnchorFrame research and interaction polish

Primary lane: `dev-cad`.

- #325 AnchorFrame root-cause research — P3.
- #81 inline rotated-occurrence AnchorFrame references — P3.
- #82 Joints-folder visibility policy — P3.
- #175 retire/consolidate historical diagnostic evidence into #325.
- #5 retire/rewrite delivered anchor scope vs remaining constraint work.

Production HUB75 work currently uses explicit Placement, so WS4 does not
preempt current P1 blockers.

## Open issue assignment — 2026-11-22

| Issue | Lane | Workstream | Disposition | Next action |
| --- | --- | --- | --- | --- |
| #5 Generic anchors and parametric constraints | `dev-cad` | WS3/WS4 | **Retire/rewrite** | Separate delivered anchor behavior from remaining constraint/associativity scope; consolidate overlap with #9. |
| #8 Tube/RectTube/OvalTube | `dev-cad` | WS3 | **P3** | Reconcile intent with native pipe/shell/boolean histories. |
| #9 First-class Sketch objects, constraints and face workplanes | `dev-cad` | WS3 | **P2 epic** | Refresh scope and deliver focused child slices. |
| #81 Inline AnchorFrame references for rotated occurrences | `dev-cad` | WS4 | **P3** | Investigate occurrence-local frames later. |
| #82 Joints folder visibility | `dev-cad` | WS4 | **P3** | Decide interaction/export policy after higher-impact defects. |
| #175 HUB75-like AnchorFrame diagnostic | `dev-cad` | WS4 | **Retire/consolidate** | Move useful evidence to #325/background docs. |
| #261 Full Forge integration runtime | `dev-ci` | WS0 | **P2 measurement-driven** | Use #637 jobs=2 result to identify the next real critical path; do not revive the old Qualification-image/matrix design. |
| #325 AnchorFrame regression root cause | `dev-cad` | WS4 | **P3 research** | Resume only when AnchorFrame becomes active. |
| #335 build123d Sheet Metal reference | `dev-cad` | WS2 | **P2** | Replace solid approximation with current sheet-metal workflow. |
| #347 Patterns accept any applied Shape feature | `dev-cad` | WS3 | **P2** | Base source validation on native history-feature identity. |
| #349 Remaining SOLID › CREATE coverage | `dev-cad` | WS1/WS3 | **P1 Revolve / P2 rest** | Split focused Revolve child for latch. |
| #354 Standalone Sketch extrusion boolean operand | `dev-cad` | WS1 | **P1** | Generalize boolean operand lowering for `sketch_base_extrusion`. |
| #355 SolidCraft 0.45 parametric native Slot dimensions | `dev-cad` | WS1 | **P1 now** | Re-derive width/length/position lowering from canonical 0.45 evidence and prove saved-design mutation. |
| #567 Mixed line/arc closed Sketch profiles | `dev-cad` | WS1 | **P1** | Deliver focused connected-curve profile API. |
| #568 Native sheet-metal flange/contour | `dev-cad` | WS1 | **P1 runtime-sensitive** | Qualify against immutable v0.3.4 contracts before exposing APIs. |
| #570 Remove CADCraft from Verification diagrams | `dev-cad` | WS2 | **P2** | Replace explanatory diagram sources with deterministic Forge-owned sources. |
| #637 Forge integration jobs=2 experiment | `dev-ci` | WS0 | **P1 now** | Adopt exact tool 0.17.0, set explicit jobs=2, measure full promotion against #636, then keep/revert based on evidence. |
| #642 Release Forge 0.11.0 | `main/release` | Release milestone | **P1 integration milestone** | After #355/#637 settle, stabilize main, reconcile changelog, verify exact release SHA, create real `v0.11.0` tag + GitHub Release, then record released baseline. |
| #643 Correct release docs and plan | `main governance` | Release milestone | **P0 now** | Merge the corrected release contract and explicit 0.11.0 milestone before further integration. |

## Immediate execution order

1. [#643] Merge the corrected release contract / v0.11.0 milestone.
2. [#355, dev-cad] Continue SolidCraft 0.45 parametric Slot qualification.
3. [#637, dev-ci] In parallel, complete the exact tool 0.17.0 / jobs=2 Forge
   integration experiment and full-promotion comparison.
4. Promote accepted lane work and leave `main` on one stable, fully verified
   CAD/runtime/CI baseline.
5. [#642] Release **Forge v0.11.0** from that exact green main SHA before
   starting another large CAD/API wave. If #355 is deliberately deferred, keep
   it out of the 0.11.0 changelog explicitly.
6. After v0.11.0, use #637 results to continue #261 and proceed with
   #354/#567/#568 and focused #349 Revolve as priorities permit.
7. Rewrite/retire #175 and #5 before treating them as implementation work.
