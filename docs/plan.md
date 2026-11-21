# Forge repository plan

This file is the current source of truth for unfinished work in
`lib.py.solidcraft.forge`.

Issues contain detail/history. Requirements and design documents own stable
contracts. This plan records the current state, ordering and disposition of all
open work.

## Current repository state

Permanent source lanes:

```text
main    18a9c279153b1a1a00dba19ce2f2e4e4fa9ef883
dev-ci  18a9c279153b1a1a00dba19ce2f2e4e4fa9ef883
dev-cad 3bf463fe579b127df2467f98f07df37c1b83661b
```

`dev-cad` is intentionally ahead after #618, which restored the Verification
Technical test details hierarchy and complete Raw test files inventory. Its
durable integration run must finish before that result is treated as published
lane evidence.

The accepted central CAD-CI stack remains:

- `lib.py.cad.ci 0.9.2` @
  `3f688243f4ee65b1fa42f82adde5344fe5101775`;
- `tool.cad.ci 0.16.1` @
  `4c6bb8b35009ef5008bd99134cf84b59fddc0b8a`;
- external named-scope acceptance: `tool.cad.ci.test` PR #61.

Durable generated scopes remain:

```text
build/main/
build/dev-cad/
build/dev-ci/
```

Generated Pages uses the corresponding stable root, `/dev-cad/` and
`/dev-ci/`. Normal PRs verify only; the destination long-lived lane performs
the durable integration update.

The public GitHub Pages source is still deliberately held on the preserved
pre-cut-over branch. #366 owns the explicit public cut-over decision.

## Runtime/reference audit state

The 2026-11-21 audit invalidated the previous assumption that SolidCraft 0.43.0
was the correct current design target merely because it was the first stable
release containing the upstream Slot-width fix.

Facts:

- immutable runtime v0.3.3 currently contains SolidCraft 0.43.0;
- that remains a factual compatibility state until a replacement runtime is
  released;
- `docs/reference/solidcraft/0.43.0/` is **not** accepted canonical reference
  evidence and must be removed by #617;
- `docker.cad.solidcraft` #21 / PR #22 is qualifying current stable
  SolidCraft 0.45.0 from the official release binary;
- Forge #619 is blocked on that owner-repository release and will create the
  canonical 0.45 reference from the released runtime;
- Forge #355 remains blocked until #619 completes.

Do not infer 0.45 contracts from the rejected 0.43 documentation.

## Priority model

- **P0 — now:** repository integrity or architecture breakage that must block
  ordinary work.
- **P1 — now/next:** concrete current blocker, regression or user-facing defect.
- **P2 — planned:** bounded improvement after P1 work.
- **P3 — later/research:** exploratory or lower-impact work.
- **Blocked:** ready in principle but waiting on an owner-repository/release
  gate.
- **Effectively complete but still open:** implementation is accepted on a dev
  lane but the issue remains open until promotion/default-branch completion.
- **Retire/rewrite:** framing is materially superseded and must be consolidated
  before implementation.

## Active workstreams

### WS0 — central CI integration and repository governance

Primary Forge lane: `dev-ci`.

- #620 is **P1 now**: re-audit cleanup safety after #604/#610/#615. Branch
  names and closed issue state must not substitute for current-SHA integration
  evidence; backup refs stay outside normal cleanup.
- #366 is **P1 decision gate**: durable build/Pages architecture exists; public
  cut-over still requires an explicit decision and verification.
- #261 is **retire/rewrite -> P2**: retain the measurable performance goal but
  rewrite it against the current released CAD-CI/runtime architecture.
- #340 is **retire**: its old squash-to-main qualification reuse model is
  superseded by long-lived lanes and direct normal-merge promotion.

#612 and #481 are closed and no longer belong in active ordering.

### WS1 — active CAD blockers

Primary lane: `dev-cad`.

- #355 is **P1 blocked** on #619: re-derive parametric native Slot behavior only
  from canonical 0.45 evidence. PR #614 was closed as superseded.
- #354 is **P1 next**: standalone sketch extrusion as a boolean operand.
- #567 is **P1 next**: mixed line/arc closed Sketch profiles needed by current
  fabrication models.
- #568 is **P1 next, runtime-sensitive**: qualify sheet-metal command contracts
  against the selected immutable current runtime before exposing them.
- #349 is **P1 for a focused Revolve child; P2 for the remaining inventory**.

### WS2 — Verification and public-site/reference truth

Primary lane: `dev-cad`.

- #574 is **effectively complete but still open**: #618 is merged to
  `dev-cad`; finish durable lane integration, then keep it open only until the
  change reaches the default branch.
- #617 is **P1 now**: delete the invalid hand-authored 0.43 reference and tighten
  the reference-capture rules. Do not change the factual package runtime pin.
- #619 is **P1 blocked** on `docker.cad.solidcraft` #21/#22: capture canonical
  0.45 evidence from the released immutable runtime.
- #621 is **P2**: generalize the canonical-reference capture/completeness rules
  after the immediate 0.43 cleanup and first compliant 0.45 capture.
- #570 is **P2**: remove CADCraft from the six explanatory Verification
  diagrams without moving generic verification rendering into Forge.
- #335 is **P2**: use real build123d sheet-metal semantics for the sheet-fold
  independent reference and clean remaining historical wording.

### WS3 — API coverage and modelling roadmap

Primary lane: `dev-cad`.

- #347 — **P2**: generalize native pattern seeds beyond Sketch extrusions.
- #9 — **P2 epic**: first-class Sketch/constraints/face workplanes; focused
  blocker #567 may land independently.
- #8 — **P3**: Tube/RectTube/OvalTube; reconcile intent with native pipe/shell
  semantics before implementation.
- #5 — **retire/rewrite**: separate already-delivered anchor behavior from the
  remaining constraint/associativity gap and consolidate overlap with #9.

### WS4 — AnchorFrame research and interaction polish

Primary lane: `dev-cad`.

- #325 — **P3 research**: current root-cause research for HUB75 AnchorFrame.
- #81 — **P3**: inline rotated-occurrence AnchorFrame references.
- #82 — **P3**: Joints-folder visibility policy.
- #175 — **retire/consolidate**: preserve useful historical diagnostic evidence
  in #325/background docs, then close or rewrite.

Production HUB75 work currently uses explicit Placement, so this work does not
preempt current P1 blockers.

## Complete open-issue assignment — 2026-11-21

| Issue | Lane | Workstream | Disposition | Next action |
| --- | --- | --- | --- | --- |
| #5 Generic anchors and parametric constraints | `dev-cad` | WS3 | **Retire/rewrite** | Separate delivered behavior from remaining constraints; consolidate with #9. |
| #8 Tube/RectTube/OvalTube | `dev-cad` | WS3 | **P3** | Reconcile with native pipe/shell/boolean histories. |
| #9 First-class Sketch objects, constraints and face workplanes | `dev-cad` | WS3 | **P2 epic** | Refresh scope; deliver focused child slices. |
| #81 Inline AnchorFrame references for rotated occurrences | `dev-cad` | WS4 | **P3** | Investigate occurrence-local frames later. |
| #82 Joints folder visibility | `dev-cad` | WS4 | **P3** | Decide interaction/export policy after higher-impact defects. |
| #175 HUB75-like AnchorFrame diagnostic | `dev-cad` | WS4 | **Retire/consolidate** | Move useful evidence to #325/background docs. |
| #261 Reduce full qualification time | `dev-ci` | WS0 | **Retire/rewrite -> P2** | Rewrite against current runtime/SCons architecture with measured target. |
| #325 AnchorFrame regression root cause | `dev-cad` | WS4 | **P3 research** | Resume only when AnchorFrame becomes active. |
| #335 build123d Sheet Metal reference | `dev-cad` | WS2 | **P2** | Replace solid approximation with current sheet-metal workflow. |
| #340 Reuse qualification after identical squash merge | `dev-ci` | WS0 | **Retire** | Close with superseded-architecture note. |
| #347 Patterns accept any applied Shape feature | `dev-cad` | WS3 | **P2** | Base source validation on native history-feature identity. |
| #349 Remaining SOLID › CREATE coverage | `dev-cad` | WS1/WS3 | **P1 Revolve / P2 rest** | Split focused Revolve child for latch. |
| #354 Standalone sketch extrusion boolean operand | `dev-cad` | WS1 | **P1 next** | Generalize boolean operand lowering. |
| #355 Parametric native Slot API | `dev-cad` | WS1 | **P1 blocked** | Wait for #619; re-derive from canonical 0.45 evidence. |
| #366 Durable output / public Pages cut-over | `dev-ci` | WS0 | **P1 decision gate** | Explicit go/no-go, then verify public/legacy routes. |
| #567 Mixed line/arc closed Sketch profiles | `dev-cad` | WS1 | **P1 next** | Deliver focused connected-curve profile API. |
| #568 Native sheet-metal flange/contour | `dev-cad` | WS1 | **P1 next / runtime-sensitive** | Qualify against selected immutable runtime first. |
| #570 Remove CADCraft from Verification diagrams | `dev-cad` | WS2 | **P2** | Replace diagram sources with deterministic Forge-owned sources. |
| #574 Technical details / complete Raw test files | `dev-cad` | WS2 | **Effectively complete but still open** | #618 merged to dev-cad; verify durable output and later promote. |
| #617 Remove invalid 0.43 reference | `dev-cad` | WS2 | **P1 now** | Delete tree and tighten canonical-reference procedure. |
| #619 Canonical SolidCraft 0.45 reference | `dev-cad` | WS2 | **P1 blocked** | Wait for immutable owner runtime, then capture complete runtime-derived reference. |
| #620 Re-audit branch cleanup safety | `dev-ci` | WS0 | **P1 now** | Reconstruct affected SHAs and restore conservative cleanup proof. |
| #621 Canonical SolidCraft reference capture/completeness rules | `dev-cad` | WS2 | **P2** | Generalize checks after #617 cleanup and the first compliant #619 capture. |

Every open issue has one primary lane and current disposition. Closed issues are
not kept in this active table.

## Parallel execution policy

- `dev-cad` and `dev-ci` progress independently.
- A running workflow blocks only work whose next step depends on that result.
- Owner-repository dependency releases are real synchronization gates.
- Generic CAD-CI behavior is fixed in its owner repository before Forge.
- Repository-wide governance may use a short-lived branch directly to `main`.

## Merge and promotion policy

- short-lived feature/fix PR -> `dev-cad` or `dev-ci`: squash;
- exact `dev-cad -> main` or `dev-ci -> main`: normal merge commit;
- every other PR to `main`: squash;
- merge method is selected only by the repository `/merge` policy workflow;
- normal cleanup applies only to explicitly temporary heads whose current
  history is proven safe; #620 re-audits the current implementation;
- permanent lanes, generated refs and backup refs are not normal cleanup
  targets.

## Immediate execution order

1. [#617, dev-cad now] Remove invalid 0.43 reference material and fix the
   reference-capture procedure.
2. [#620, dev-ci now] Re-audit branch cleanup safety in parallel.
3. [runtime owner gate] Finish `docker.cad.solidcraft` #21/#22 and publish the
   selected immutable runtime only after its exact checks pass.
4. [#619, dev-cad blocked] Capture canonical 0.45 reference from that released
   runtime.
5. [#355, dev-cad blocked] Re-derive Slot support from #619 evidence.
6. [#366, dev-ci decision gate] Decide the public Pages cut-over explicitly.
7. Continue #354/#567/#568 and the focused #349 Revolve child as dependencies
   permit.
