# Forge repository plan

This file is the current source of truth for unfinished work in
`lib.py.solidcraft.forge`.

Permanent requirements/design/API/release contracts belong in the primary
documents in `docs/`. Issues keep implementation detail and history.

## Current repository state

Permanent source lanes:

```text
main
dev-cad
dev-ci
```

The lanes intentionally diverge while work is active. Do not record one
hard-coded global baseline SHA here. Use the live branch heads and durable
`build/<lane>/build.json.source_commit` manifests for exact identity.

The current accepted generic CI stack is:

- `lib.py.cad.ci 0.9.3` @
  `74486c441f1f2b170ff3dc06e0edcaf662fbec6b`;
- `tool.cad.ci 0.16.2` @
  `59e4c4d3f377f906b33bb2d1fee808f96c6fb1b9`;
- external black-box acceptance: `tool.cad.ci.test` #62 / PR #63.

Forge consumer evidence measured the pre-target interval dropping from
26.507 s on tool 0.16.1 / lib 0.9.2 to 1.375 s on 0.16.2 / 0.9.3. The
structural owner-layer contract, not that timing number, remains authoritative.

The current immutable CAD runtime is:

- `docker.cad.solidcraft v0.3.4`;
- exact runtime source commit
  `89acce00bd760c523251c6c84d291d758c2a4dc5`;
- `solidcraft-cli 0.45.0`;
- immutable roles `cad-solidcraft:v0.3.4` and
  `cad-reference:v0.3.4`.

Runtime v0.3.3 / SolidCraft 0.43.0 remains historical immutable evidence only.

Generated durable scopes remain:

```text
build/main/
build/dev-cad/
build/dev-ci/
```

Generated Pages uses the matching stable root, `/dev-cad/` and `/dev-ci/`.
Public Pages has already been cut over to generated `gh-pages`; #366 is
complete and is not an active decision gate.

Repository cleanup safety is complete under #481: automatic cleanup requires
current-SHA integration proof or an exact merged-PR-head SHA. Closed issue state
and `backup/*` are not general deletion evidence.

## Lane rule

A dependency handoff does not move work between lanes.

- `dev-ci` owns Forge CI/infrastructure/runtime-consumer/publication work.
- `dev-cad` owns Forge API/compiler/model/reference/Verification work.
- Generic CAD-CI behavior is fixed/released in its owner repository first.
- Runtime construction/release is fixed in `docker.cad.solidcraft` first.
- Blocked CAD work remains CAD work.

Short-lived feature/fix PRs target one dev lane and are squash-merged.

Direct promotion is only:

```text
dev-cad -> main
dev-ci  -> main
```

Those exact permanent-lane promotions use a normal merge commit through the
repository `/merge` policy. Every other PR to `main` is squash-merged.

## Current workstreams

### WS0 — CI and repository integration

Primary lane: `dev-ci`.

No Forge CI migration is currently blocking CAD work. The accepted
0.16.2 / 0.9.3 stack and runtime v0.3.4 are already on `main`.

Central tool work may continue independently:
- `tool.cad.ci` #76 is exposing already library-owned bounded SCons jobs;
- Forge must not consume that surface until an exact released tool revision has
  passed `tool.cad.ci.test`;
- default serial behavior remains `jobs=1` until a consumer explicitly opts in.

Forge #261 is retained as a performance goal but must be rewritten against the
current SCons/runtime architecture before implementation.

### WS1 — active CAD blockers

Primary lane: `dev-cad`.

1. #617 canonical SolidCraft 0.45 reference — active now.
2. #355 parametric native Slot API — next after #617 canonical evidence.
3. #354 standalone Sketch extrusion as boolean operand.
4. #567 mixed line/arc closed Sketch profiles.
5. #568 native sheet-metal flange/contour features.
6. #349 focused Revolve child first; remaining SOLID › CREATE inventory later.

### WS2 — Verification and reference truth

Primary lane: `dev-cad`.

- #574 is accepted on `dev-cad`: #618 restored the complete Technical test
  details / Raw test files hierarchy. It remains open until promoted to the
  default branch and stable Pages is verified.
- #617 removes the noncanonical 0.43 reference and captures the canonical 0.45
  registry directly from immutable runtime v0.3.4.
- #570 removes the remaining CADCraft dependency from explanatory Verification
  diagrams without moving generic rendering into Forge.
- #335 updates the sheet-fold independent build123d reference.

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

## Open issue assignment — 2026-11-21

| Issue | Lane | Workstream | Disposition | Next action |
| --- | --- | --- | --- | --- |
| #5 Generic anchors and parametric constraints | `dev-cad` | WS3/WS4 | **Retire/rewrite** | Separate delivered anchor behavior from remaining constraint/associativity work; consolidate overlap with #9. |
| #8 Tube/RectTube/OvalTube | `dev-cad` | WS3 | **P3** | Reconcile intent with native pipe/shell/boolean histories. |
| #9 First-class Sketch objects, constraints and face workplanes | `dev-cad` | WS3 | **P2 epic** | Refresh scope and deliver focused child slices. |
| #81 Inline AnchorFrame references for rotated occurrences | `dev-cad` | WS4 | **P3** | Investigate occurrence-local frames later. |
| #82 Joints folder visibility | `dev-cad` | WS4 | **P3** | Decide interaction/export policy after higher-impact defects. |
| #175 HUB75-like AnchorFrame diagnostic | `dev-cad` | WS4 | **Retire/consolidate** | Move useful evidence to #325/background docs. |
| #261 Reduce full qualification time | `dev-ci` | WS0 | **Retire/rewrite → P2** | Rewrite against current SCons/runtime architecture and measured promotion profiles. |
| #325 AnchorFrame regression root cause | `dev-cad` | WS4 | **P3 research** | Resume only when AnchorFrame becomes active. |
| #335 build123d Sheet Metal reference | `dev-cad` | WS2 | **P2** | Replace solid approximation with current sheet-metal workflow. |
| #340 Reuse qualification after identical squash merge | `dev-ci` | WS0 | **Retire** | Close with superseded-architecture note. |
| #347 Patterns accept any applied Shape feature | `dev-cad` | WS3 | **P2** | Base source validation on native history-feature identity. |
| #349 Remaining SOLID › CREATE coverage | `dev-cad` | WS1/WS3 | **P1 Revolve / P2 rest** | Split focused Revolve child for latch. |
| #354 Standalone Sketch extrusion boolean operand | `dev-cad` | WS1 | **P1** | Generalize boolean operand lowering. |
| #355 Parametric native Slot API | `dev-cad` | WS1 | **P1 next** | Re-derive from canonical #617 SolidCraft 0.45 evidence; do not reuse 0.43 assumptions. |
| #567 Mixed line/arc closed Sketch profiles | `dev-cad` | WS1 | **P1** | Deliver focused connected-curve profile API. |
| #568 Native sheet-metal flange/contour | `dev-cad` | WS1 | **P1 runtime-sensitive** | Qualify against immutable v0.3.4 contracts before exposing APIs. |
| #570 Remove CADCraft from Verification diagrams | `dev-cad` | WS2 | **P2** | Replace explanatory diagram sources with deterministic Forge-owned sources. |
| #574 Technical details / complete Raw test files | `dev-cad` | WS2 | **P1 promotion pending** | #618 is accepted on dev-cad; retain it through lane sync, then promote and verify stable Pages. |
| #617 Canonical SolidCraft 0.45 reference | `dev-cad` | WS1/WS2 | **P1 now** | Revalidate PR #634 after this main→dev-cad synchronization, merge to dev-cad, then durable proof. |

Every open issue has one primary lane and current disposition. Closed issues are
not kept in the active table.

## Immediate execution order

1. [#617, dev-cad] Revalidate canonical 0.45 runtime-derived evidence on the
   synchronized lane, then merge and prove durable dev-cad output.
2. [#355, dev-cad] Re-derive Slot qualification from the accepted 0.45 evidence.
3. [#574, dev-cad] Keep the already accepted Verification evidence layout intact
   and promote it with the next suitable dev-cad → main promotion.
4. [central CI, parallel] Finish/release/externally accept tool #76 bounded jobs
   before any Forge jobs>1 experiment.
5. Continue #354/#567/#568 and focused #349 Revolve work as dependencies permit.
6. Rewrite/retire #261/#340/#175/#5 before treating them as implementation.
