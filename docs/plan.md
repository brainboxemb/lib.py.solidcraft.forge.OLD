# Forge repository plan

This file is the current source of truth for unfinished work in
`lib.py.solidcraft.forge`.

Permanent requirements/design/API/release contracts belong in the primary
documents in `docs/`. Issues keep implementation detail and history.

## Current status

The development-lane migration (#572) and backlog reorganization (#578) are
complete.

Permanent source lanes:

```text
main
dev-cad
dev-ci
```

The long-lived lanes intentionally diverge while work is active. Do not record a
single hard-coded "current baseline" SHA here; use the live GitHub branch heads
and durable `build/<lane>/build.json.source_commit` manifests for identity.

The current externally accepted generic stack is:

- `lib.py.cad.ci 0.9.3` @
  `74486c441f1f2b170ff3dc06e0edcaf662fbec6b`;
- `tool.cad.ci 0.16.2` @
  `59e4c4d3f377f906b33bb2d1fee808f96c6fb1b9`;
- external acceptance: `tool.cad.ci.test` #62 / PR #63, including the
  selective active-closure regression proof.

The generated `build` branch is now clean and contains exactly:

```text
main/
dev-cad/
dev-ci/
```

At that synchronization point each scope was a complete 188-item baseline.
During active development, each named scope records its own accepted
`source_commit` and may legitimately be ahead of `main` until promotion.

Generated Pages records the matching scope at the stable root, `/dev-cad/`
and `/dev-ci/`.

Normal short-lived PRs target one dev lane, verify only and are squash-merged.
The destination dev push is the durable integration event.

Promotion is direct from the long-lived lane:

```text
dev-cad -> main
dev-ci  -> main
```

Promotion PRs run complete validation and are merged through the repository
merge-policy workflow. The merge method is selected mechanically:

- base `main` + head exactly `dev-cad` or `dev-ci` -> normal merge commit;
- every other PR -> squash merge.

Temporary `promote/*` heads are no longer part of the supported promotion
flow. After a direct lane promotion, the merge-policy workflow ensures that the
long-lived lane ref still exists and points at the resulting main merge commit,
even when GitHub's repository setting auto-deletes merged head branches.
Named-lane incremental selection uses the previous durable
`build/<lane>/build.json.source_commit`, not `github.event.before`.

Public GitHub Pages has already been cut over to the generated `gh-pages`
branch. #366 is complete; there is no remaining live Pages go/no-go gate.

#481 is reopened as a P0 repository-integrity correction after the 2026-11-21
audit found that #604/#610/#615 weakened the conservative cleanup contract.
Corrective PR #626 is accepted on `dev-ci`; direct promotion #629 must land
before any further `/cleanup-branches` command is used. A historical Pages
rollback ref is branch-history material, not an active publication decision gate.

Docs-only pull-request classification (#576) is complete. Acceptance run
`44904510041` kept the normal `cad_ci_pr` check green while skipping the
released CAD-CI action entirely for a `docs/plan.md`-only PR. Promotion PRs
to `main` still bypass that shortcut and require complete validation.

Runtime v0.3.3 / SolidCraft 0.43.0 remains immutable historical evidence only.
Runtime owner `docker.cad.solidcraft` has now released **v0.3.4** from exact
green main commit `89acce00bd760c523251c6c84d291d758c2a4dc5`; both immutable
runtime roles are built/smoke-tested and the SolidCraft role contains exact
`solidcraft-cli 0.45.0`.

Forge must now adopt only the immutable v0.3.4 runtime pins and tested
SolidCraft version through `dev-ci`. Canonical 0.45 reference capture and
Forge API/compiler/qualification work remain on `dev-cad`; the discarded
hand-authored 0.43 reference material is not evidence.

## Priority model

The backlog uses five dispositions:

- **P0 — now:** finish the active architecture/migration or an immediate
  repository-governance task before ordinary feature work.
- **P1 — next:** concrete current blocker, regression or user-facing defect
  with a known downstream need.
- **P2 — planned:** valuable bounded improvement or roadmap item that should
  follow the P1 blockers.
- **P3 — later/research:** strategic, exploratory or polish work without a
  current delivery blocker.
- **Retire/rewrite:** issue framing is materially superseded, duplicated or
  based on the retired Qualification/CI architecture. Preserve useful evidence,
  then close, consolidate or rewrite before implementation.

The lane column below is the **Forge integration lane**. Generic CAD-CI work
still belongs in `lib.py.cad.ci` / `tool.cad.ci` first, even when Forge
consumes it through `dev-ci`.

## Workstreams

### WS0 — Repository, CI and publication

Primary lane: `dev-ci`.

Owns source-branch topology, generated-state lifecycle, CI cost/reliability,
runtime/tooling simplification and operational Pages publication.

Immediate order:

1. #633 adopt the externally accepted CAD-CI 0.16.2 / lib 0.9.3 stack on
   `dev-ci` and capture the real Forge pre-target startup interval;
2. verify the durable `dev-ci` scope after the accepted repin;
3. promote #633 separately to `main` through the direct lane path;
4. rewrite the still-useful performance goal from #261 against the current
   released CAD-CI/runtime architecture.

### WS1 — Active CAD blockers and developer UX

Primary lane: `dev-cad`.

These are concrete blockers found in current HUB75/latch work and should be
handled before broad coverage expansion:

1. #355 parametric native Slot support — `dev-cad`, blocked only until the
   released v0.3.4 / SolidCraft 0.45.0 runtime pin is adopted and #617 provides
   canonical 0.45 reference evidence;
2. #354 standalone sketch extrusion as a boolean operand;
3. #567 connected line/arc Sketch profiles for sheet-metal blanks;
4. #568 native sheet-metal flange/contour features;
5. #349: split out **Revolve** as the first focused child because the latch
   needs it; keep the rest of the broad SOLID › CREATE inventory in WS3.

#357 and #356 are complete and no longer belong in the open-work ordering.

This order may be adjusted when one downstream model proves a harder direct
dependency, but broad API expansion must not displace known blockers.

### WS2 — Verification and public-site quality

Primary lane: `dev-cad`. Presentation, reference truth and Forge-owned
Verification content belong here; only generic CI/runtime mechanics discovered
during the work move to `dev-ci` or the central CAD-CI repositories.

- #574 is P1 promotion-pending: #618 is accepted on `dev-cad`; promote and
  verify stable Pages.
- #570 is P2: remove the remaining CADCraft dependency from the six explanatory
  Verification diagrams without moving generic verification rendering into Forge.
- #335 is P2: make the sheet-fold build123d reference use real sheet-metal
  semantics and rewrite remaining historical Qualification wording.

### WS3 — API coverage and modelling roadmap

Primary lane: `dev-cad`.

- #347 generalize native pattern seeds beyond Sketch extrusions — P2.
- #9 first-class Sketch/constraints/face workplanes — P2 strategic epic;
  focused blocker #567 may land first without waiting for the entire epic.
- #349 remaining SOLID › CREATE coverage after the focused Revolve slice — P2.
- #8 Tube/RectTube/OvalTube — P3; coordinate with native `solid.pipe`
  coverage rather than inventing a parallel geometry engine.

### WS4 — AnchorFrame research and interaction polish

Primary lane: `dev-cad`.

This work is intentionally behind the current blockers because production
HUB75 uses explicit Placement today.

- #325 AnchorFrame regression root-cause research — P3.
- #81 inline rotated-occurrence AnchorFrame references — P3.
- #82 Joints-folder visibility policy — P3.
- #175 contains useful historical diagnostic evidence but overlaps #325 and
  the completed change-0005 history; consolidate that evidence, then close or
  rewrite #175.
- #5 predates much of the current Anchor/Placement/AnchorFrame implementation
  and substantially overlaps #9; rewrite it to the remaining unsolved
  constraint/associativity gap or consolidate it into #9.

## Complete open-issue assignment — 2026-11-21

| Issue | Lane | Workstream | Priority | Next action |
| --- | --- | --- | --- | --- |
| #481 Remove stale Forge development branches | `dev-ci` | WS0 | **P0 audit fix** | #626 is accepted on dev-ci; promote #629 to main before cleanup is used again. Current-tip integration or exact merged-PR head SHA is required; issue state and backup refs are never general deletion evidence. |
| #630 Adopt immutable runtime v0.3.4 / SolidCraft 0.45.0 | `dev-ci` | WS0 | **P1 now** | Update only both immutable runtime-role pins and Forge/CI tested SolidCraft version; keep #355 and #617 on dev-cad. |
| #570 Remove CADCraft from Forge verification diagrams | `dev-cad` | WS2 | **P2** | Replace the six explanatory diagram sources with deterministic Forge-owned SVG/static sources; remove its CI/runtime input only after the content path no longer needs it. |
| #261 Reduce full qualification from minutes to seconds | `dev-ci` | WS0 | **Retire/rewrite → P2** | Original Qualification/image plan is obsolete; retain measured-performance goal and rewrite against current runtime images, batching and SCons execution. |
| #340 Reuse full release qualification after identical squash merge | `dev-ci` | WS0 | **Retire** | Old Qualification + squash-to-main model is superseded by long-lived lanes and normal promotion merges; close with historical note. |
| #355 Support current SolidCraft parametric Slot API in Forge | `dev-cad` | WS1 | **P1 blocked on adoption/reference** | Runtime v0.3.4 / SolidCraft 0.45.0 is released; after dev-ci pin adoption and #617 canonical evidence, revalidate Slot width and continue native dimension/constraint lowering. |
| #354 Support standalone sketch extrusions as boolean operands | `dev-cad` | WS1 | **P1** | Generalize boolean operand lowering for `sketch_base_extrusion`. |
| #567 Mixed line/arc closed Sketch profiles for sheet-metal blanks | `dev-cad` | WS1 | **P1** | Deliver focused connected-curve profile API; do not wait for all of #9. |
| #568 Native sheet-metal flange and contour features | `dev-cad` | WS1 | **P1** | Qualify the required contracts against the selected current immutable SolidCraft runtime and expose generic fabrication-intent APIs. |
| #349 Remaining SolidCraft SOLID › CREATE coverage | `dev-cad` | WS1/WS3 | **P1 Revolve; P2 remainder** | Split focused Revolve child for latch; retain parent as truthful coverage inventory. |
| #574 Restore Technical test details hierarchy and complete Raw test files | `dev-cad` | WS2 | **P1 promotion pending** | #618 is accepted on dev-cad and the generated sheet-fold page exposes 60 structured file links; keep open until promoted to main and stable Pages is verified. |
| #617 Replace incomplete 0.43 command reference with canonical current-runtime snapshot | `dev-cad` | WS2 | **P1 now** | Remove the hand-authored 0.43 tree and capture complete `solidcraft-cli commands` evidence from released runtime v0.3.4; raw registry is canonical, Markdown is generated. |
| #335 Use build123d Sheet Metal for sheet-fold reference | `dev-cad` | WS2 | **P2** | Replace solid approximation with current build123d Sheet Metal workflow and update historical terminology/tests. |
| #347 Patterns accept any applied Shape feature | `dev-cad` | WS3 | **P2** | Base source validation on native history-feature identity; qualify Hole + sketch-extrude seeds. |
| #9 First-class Sketch objects, constraints and face workplanes | `dev-cad` | WS3 | **P2 epic** | Refresh scope against current Sketch/attachment capabilities; use focused child issues for deliverable slices. |
| #8 Generic hollow primitives Tube/RectTube/OvalTube | `dev-cad` | WS3 | **P3** | Reconcile public shape intent with native `solid.pipe`/shell/boolean histories before implementation. |
| #325 HUB75 AnchorFrame regression root-cause research | `dev-cad` | WS4 | **P3 research** | Rebuild diagnostic from current foundation only when AnchorFrame work becomes active again. |
| #175 HUB75-like AnchorFrame orientation diagnostic | `dev-cad` | WS4 | **Retire/consolidate** | Move still-useful historical evidence to #325/background docs, then close or rewrite. |
| #81 Inline AnchorFrame references for rotated occurrences | `dev-cad` | WS4 | **P3** | Investigate native occurrence-local inline frames without adding a generic matrix engine. |
| #82 Reconsider automatic hiding of SolidCraft Joints folder | `dev-cad` | WS4 | **P3** | Decide interactive/export visibility policy after higher-impact modelling defects. |
| #5 Generic anchors and parametric constraints | `dev-cad` | WS3/WS4 | **Retire/rewrite** | Separate already-delivered anchor behavior from remaining constraint/associativity work; consolidate overlap with #9. |

Every open issue has one primary lane and disposition. New issues should be
added to this table when they become active planning inputs; issue history is
not a substitute for this plan.

## Parallel execution policy

The two long-lived development lanes are independent execution tracks.

- `dev-cad` and `dev-ci` may progress in parallel.
- A running workflow blocks only work whose next step depends on its result.
  Do not idle the other lane merely because one lane is validating or
  publishing.
- Shared dependency releases, owner-repository handoffs and true architecture
  synchronization points remain dependency gates.
- Repository-wide governance that applies equally to both lanes may use a
  short-lived branch directly against `main`.
- Governance-only PRs to `main` are squash-merged.
- Do not choose a merge method manually. Repository automation must use the
  policy-controlled merge workflow from #598.

## Merge and promotion policy

- Short-lived feature/fix PRs target `dev-cad` or `dev-ci` and are
  **squash-merged**.
- PRs to `main` are **squash-merged by default**.
- The only normal-merge exception is a PR whose head is literally the
  long-lived `dev-cad` or `dev-ci` branch and whose base is `main`.
- Temporary heads such as `promote/dev-cad`, `promote/dev-ci`, governance
  branches and all other short-lived heads are squash-merged.
- Promotion PRs require complete processed validation.
- Merge method selection is not a human/assistant choice. Once #598 lands,
  repository automation must merge through the policy-controlled `/merge`
  path; direct merge calls are unsupported.
- After a direct lane promotion, the policy workflow restores/synchronizes the
  promoted long-lived branch to the resulting main merge commit if GitHub's
  automatic head-branch deletion removed it.
- The other long-lived lane incorporates main separately; it is never reset
  over unpromoted work.
- Named lane incremental selection uses the prior durable
  `build/<lane>/build.json.source_commit` as base, not
  `github.event.before`.
- A PR never publishes durable build or Pages state; the destination
  development-branch push performs the durable integration update.

## Immediate execution order

1. [dev-ci #633] Adopt externally accepted CAD-CI 0.16.2 / lib 0.9.3 and
   measure the real Forge selective startup interval.
2. [dev-cad #617] Capture the canonical 0.45 command registry from released
   runtime v0.3.4 and remove the noncanonical 0.43 tree.
4. [dev-cad #355] Re-derive Slot qualification from the 0.45 evidence.
5. [dev-cad #574] Promote the accepted Technical test details/evidence layout
   and verify stable Pages.
6. Continue #354/#567/#568 and the focused #349 Revolve work as dependencies
   permit; rewrite/retire #261/#340/#175/#5 before implementation.
