# Forge repository plan

This file is the current source of truth for unfinished work in
`lib.py.solidcraft.forge`.

Forge has two parallel responsibility areas that must both remain visible in
planning and handoffs:

1. the **CAD library itself** — public API, compiler/lowering, modelling
   semantics, examples, native qualification and model-specific verification;
2. the **CI/verification/runtime integration around that library** — generic
   CAD-CI consumption, durable build/Page publication, verification package
   integration, runtime-image consumption and release mechanics.

Neither area is subordinate to the other. `dev-cad` and `dev-ci` are separate
execution lanes for these two concerns and should progress independently when
there is no real dependency between them.

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
- `tool.cad.ci 0.17.0` @
  `d88d6e189c12edb5a30158c068145c099c17a019`;
- external jobs=2 acceptance: `tool.cad.ci.test` #66 / PR #67;
- Forge explicitly uses `jobs=2` on PR and durable integration runs.

Forge performance evidence:

- selective startup improved from 26.507 s on tool 0.16.1 / lib 0.9.2 to
  1.375 s on tool 0.16.2 / lib 0.9.3;
- jobs=1 full promotion #636: 4m54s;
- jobs=2 #645 first run: 4m44s;
- jobs=2 #645 exact-SHA rerun: 3m12s;
- the clean jobs=2 rerun measured 7.015 s pre-target, 62.238 s model
  verification and 59.616 s reference verification with the heavy batches
  overlapping.

The structural owner-layer contract remains authoritative. Timing values are
diagnostic evidence and runner/image-pull variance remains material.

## Repository-entrypoint correction

Issue #649 is **P0 now** governance work. `AGENTS.md` is currently stale and
contradicts the accepted runtime, CAD-CI, Pages and release state. Correct it
before further implementation so a fresh handoff cannot restart from retired
architecture. This correction does not wait for #355 because it changes only
repository-wide instructions.

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
- #637 / #645: exact tool.cad.ci 0.17.0 with explicit jobs=2 accepted and
  promoted by normal dev-ci -> main merge; durable main/dev-ci build and Pages
  publication are green.
- #643 / #644: release documentation corrected and Forge v0.11.0 made an
  explicit real-tag/GitHub-Release milestone.

## Lane rule

The repository deliberately has two concurrent work lanes:

- `dev-cad` owns the Forge CAD library: API/compiler/model semantics,
  references, qualification/Verification content and CAD-facing behavior;
- `dev-ci` owns the infrastructure around that library: Forge CI integration,
  runtime-consumer wiring, durable build state and publication.
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

Release v0.11.0 is planned after the current CAD integration settles:

- #355 reaches an accepted/promoted state, or is explicitly deferred from
  0.11.0 with the changelog reflecting that decision;
- the jobs=2 CI experiment is already resolved: main now uses the accepted
  tool.cad.ci 0.17.0 / lib.py.cad.ci 0.9.3 stack with jobs=2.

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

#637 is complete. Forge now uses exact tool.cad.ci 0.17.0 / lib.py.cad.ci
0.9.3 with explicit jobs=2.

#261 is the next measurement-driven CI work, but it does not preempt #355 or the
v0.11.0 integration milestone. Its next investigation is:

1. separate immutable-image pull time from container execution across repeated
   promotion-equivalent runs;
2. explain the large reference-image pull variance;
3. identify the remaining serial SCons tail after model/reference batches;
4. fix only the owner layer of the dominant cost;
5. do not increase the jobs bound beyond 2 without separate evidence.

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
| #261 Full Forge integration runtime | `dev-ci` | WS0 | **P2 measurement-driven** | Measure image-pull/runner variance and the remaining serial tail on the accepted jobs=2 stack; do not increase jobs or revive the old Qualification-image/matrix design without evidence. |
| #325 AnchorFrame regression root cause | `dev-cad` | WS4 | **P3 research** | Resume only when AnchorFrame becomes active. |
| #335 build123d Sheet Metal reference | `dev-cad` | WS2 | **P2** | Replace solid approximation with current sheet-metal workflow. |
| #347 Patterns accept any applied Shape feature | `dev-cad` | WS3 | **P2** | Base source validation on native history-feature identity. |
| #349 Remaining SOLID › CREATE coverage | `dev-cad` | WS1/WS3 | **P1 Revolve / P2 rest** | Split focused Revolve child for latch. |
| #354 Standalone Sketch extrusion boolean operand | `dev-cad` | WS1 | **P1** | Generalize boolean operand lowering for `sketch_base_extrusion`. |
| #355 SolidCraft 0.45 parametric native Slot dimensions | `dev-cad` | WS1 | **P1 now** | Re-derive width/length/position lowering from canonical 0.45 evidence and prove saved-design mutation. |
| #567 Mixed line/arc closed Sketch profiles | `dev-cad` | WS1 | **P1** | Deliver focused connected-curve profile API. |
| #568 Native sheet-metal flange/contour | `dev-cad` | WS1 | **P1 runtime-sensitive** | Qualify against immutable v0.3.4 contracts before exposing APIs. |
| #570 Remove CADCraft from Verification diagrams | `dev-cad` | WS2 | **P2** | Replace explanatory diagram sources with deterministic Forge-owned sources. |
| #642 Release Forge 0.11.0 | `main/release` | Release milestone | **P1 integration milestone** | After #355 is accepted/promoted or explicitly deferred, stabilize main, reconcile changelog, verify exact release SHA, create real `v0.11.0` tag + GitHub Release, then record released baseline. |
| #643 Correct Forge release documentation | `main governance` | Release milestone | **effectively complete but still open** | `docs/release.md` and this plan already contain the corrected contract; close after confirming merged state. |
| #647 Reconcile plan after jobs=2 promotion | `main governance` | WS0 | **effectively complete but still open** | The accepted jobs=2 state is already recorded on main; close after confirming merged state. |
| #649 Refresh AGENTS.md current architecture | `main governance` | Repository entrypoint | **P0 now** | Align AGENTS with runtime v0.3.4 / SolidCraft 0.45.0, CAD-CI 0.17.0/0.9.3 jobs=2, live Pages, `/merge` policy and the real release contract. |

## Immediate execution order

1. [#649, main governance] Correct `AGENTS.md` so new handoffs start from the
   current architecture and cannot mistake source version `0.11.0` for a real
   release.
2. Close administratively complete governance issues such as #643/#647 after
   verifying their merged state.
3. [#355, dev-cad] Finish SolidCraft 0.45 parametric Slot native baseline and
   saved-design mutation qualification, update public API docs, merge to
   dev-cad, prove durable lane output, then promote to main.
4. [#642] Release **Forge v0.11.0** from one exact green main SHA after #355 is
   promoted, or explicitly defer #355 and keep it out of the 0.11.0 changelog.
5. After v0.11.0, continue #261 image-pull/serial-tail investigation and proceed
   with #354/#567/#568 and focused #349 Revolve as priorities permit.
6. Rewrite/retire #175 and #5 before treating them as implementation work.
