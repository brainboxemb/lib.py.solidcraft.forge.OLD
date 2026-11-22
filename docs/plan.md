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

## Recently completed default-branch work

- #574 / PR #618: complete Verification Technical test details / Raw test files
  hierarchy.
- #617 / PR #634 and promotion #638: canonical SolidCraft 0.45 reference from
  immutable runtime v0.3.4.
- #637 / #645: exact tool.cad.ci 0.17.0 with explicit jobs=2 accepted and
  promoted through the normal `dev-ci -> main` merge.
- #643 / #644: release documentation corrected; source version `0.11.0` is
  explicitly not treated as a release.
- #649 / #650: repository handoff/AGENTS corrected to describe both the CAD
  library and CI/integration responsibilities.
- #355 / #646 / #651: SolidCraft 0.45 parametric native Slot support accepted
  on `dev-cad`, promoted to `main` by normal merge commit
  `92758bd34b8b83bcfe28180b8ae2d42c3338f215`, and proven by green durable
  main build + stable Pages on that exact SHA.

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

The two pre-release integration gates are resolved at source level:

- #355 is complete on main with matching durable build/Page evidence;
- the jobs=2 CI experiment is resolved: main uses accepted tool.cad.ci 0.17.0 /
  lib.py.cad.ci 0.9.3 with jobs=2.

Release execution is now the only `now` work:

1. require durable `build/main` and stable Pages to point to the accepted
   post-#651 main source;
2. audit all public changes since `v0.10.0` and reconcile `[Unreleased]`;
3. create one release-preparation PR that leaves a fresh `[Unreleased]` and
   creates the dated `[0.11.0]` section only immediately before publication;
4. require complete release-candidate verification on the exact resulting
   green main SHA;
5. create immutable tag `v0.11.0` at that SHA;
6. create the GitHub Release;
7. verify tag and GitHub Release both resolve to that SHA;
8. record the released baseline here before the next large development wave.

A changelog heading or package version is not a release.

### WS0 — CI performance and integration

Primary lane: `dev-ci`.

#637 is complete. Forge now uses exact tool.cad.ci 0.17.0 / lib.py.cad.ci
0.9.3 with explicit jobs=2.

#261 is the next measurement-driven CI work after v0.11.0. It may proceed in
parallel with post-release CAD work. Its next investigation is:

1. separate immutable-image pull time from container execution across repeated
   promotion-equivalent runs;
2. explain the large reference-image pull variance;
3. identify the remaining serial SCons tail after model/reference batches;
4. fix only the owner layer of the dominant cost;
5. do not increase the jobs bound beyond 2 without separate evidence.

### WS1 — next CAD-library work

Primary lane: `dev-cad`.

#355 is implemented and promoted. After v0.11.0, resume independent CAD-library
work in this order unless new evidence changes the dependency chain:

1. #354 standalone Sketch extrusion as boolean operand;
2. #567 mixed line/arc closed Sketch profiles;
3. #568 native sheet-metal flange/contour features;
4. #349 focused Revolve child first; remaining SOLID › CREATE inventory later.

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

Every currently open issue is explicitly classified below. Priority and lane are
secondary to the disposition: `now`, `next`, `later`, `blocked`,
`probably obsolete`, or `effectively complete but still open`.

| Issue | Lane | Disposition | Next action |
| --- | --- | --- | --- |
| #5 Generic anchors and parametric constraints | `dev-cad` | **probably obsolete** | Rewrite around the still-missing constraint/associativity scope and consolidate overlap with #9 before implementation. |
| #8 Tube/RectTube/OvalTube | `dev-cad` | **later** | Reconcile intent with native pipe/shell/boolean histories. |
| #9 First-class Sketch objects, constraints and face workplanes | `dev-cad` | **later** | Refresh the epic and deliver focused child slices. |
| #81 Inline AnchorFrame references for rotated occurrences | `dev-cad` | **later** | Investigate occurrence-local frames only when AnchorFrame work becomes active. |
| #82 Joints folder visibility | `dev-cad` | **later** | Decide interaction/export policy after higher-impact CAD defects. |
| #175 HUB75-like AnchorFrame diagnostic | `dev-cad` | **probably obsolete** | Consolidate retained evidence into #325/background documentation, then close or rewrite. |
| #261 Full Forge integration runtime | `dev-ci` | **next** | After v0.11.0, measure image-pull/runner variance and remaining serial tail on jobs=2 before changing concurrency. |
| #325 AnchorFrame regression root cause | `dev-cad` | **later** | Resume only when AnchorFrame is an active product/API dependency. |
| #335 build123d Sheet Metal reference | `dev-cad` | **later** | Replace the solid approximation with current build123d sheet-metal semantics. |
| #347 Patterns accept any applied Shape feature | `dev-cad` | **later** | Base source validation on native history-feature identity. |
| #349 Remaining SOLID › CREATE coverage | `dev-cad` | **next** | Split focused Revolve child for the latch; leave broad inventory for later. |
| #354 Standalone Sketch extrusion boolean operand | `dev-cad` | **next** | Generalize boolean operand lowering for `sketch_base_extrusion`. |
| #567 Mixed line/arc closed Sketch profiles | `dev-cad` | **next** | Deliver focused connected-curve profile API after the release gate. |
| #568 Native sheet-metal flange/contour | `dev-cad` | **next** | Qualify immutable v0.3.4 native contracts before exposing APIs. |
| #570 Remove CADCraft from Verification diagrams | `dev-cad` | **later** | Replace explanatory diagram sources without moving generic verification rendering into Forge. |
| #642 Release Forge 0.11.0 | `main/release` | **now** | Finish main durability gate, reconcile release notes, verify one exact main SHA, create real tag + GitHub Release, and record the baseline. |

## Immediate execution order

1. [#642] Reconcile the release changelog against all public changes since
   `v0.10.0`; do not mistake the historical source-only “Release SCPF 0.11.0”
   commit for a real release.
2. [#642] Publish **Forge v0.11.0** only from one exact green `main` SHA with
   matching durable build/Page evidence, immutable tag and GitHub Release.
3. After v0.11.0, run #261 on `dev-ci` and #354/#567/#568/focused #349 on
   `dev-cad` independently where dependencies permit.
4. Rewrite/retire #175 and #5 before treating them as implementation work.
