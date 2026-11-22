# 0042 — SolidCraft 0.45 parametric native Slot dimensions

Status: **implemented and natively qualified on the feature branch; repository merge pending**  
Issue: **#355**  
SolidCraft target: **0.45.0**  
Runtime: **docker.cad.solidcraft v0.3.4**

## Problem

Change 0027 introduced the five native Slot constructors against SolidCraft
0.42 and deliberately kept direct Slot points and width numeric. That was the
correct contract for that runtime, but it is no longer the current SolidCraft
contract.

The canonical SolidCraft 0.45 registry and source now distinguish two authoring
boundaries:

- direct `sketch.slot.*` point fields are still numeric `PlainPoint` values;
- direct Slot `width` accepts a number or expression;
- `sketch.draw.dimensioned` can create the same native straight Slot while
  driving its `length` / `width` roles and returning `centre_line` /
  `middle` handles for later native constraints.

Forge must expose that capability without sending symbolic values into native
point fields and without replacing Slot geometry with rounded rectangles.

## Decision

All five public Slot constructors accept a numeric or symbolic width.

The three straight constructors additionally accept parameterized authored
endpoints when the current axis is horizontal or vertical.

Forge lowers those straight Slots as follows:

1. retain the authored Parameter/Expression intent in Forge;
2. evaluate current values only to create numeric native seed points;
3. wrap the same native Slot creator in `sketch.draw.dimensioned`;
4. drive the SolidCraft 0.45 `length` role from the authored axis intent;
5. bind the returned `centre_line` and `middle`;
6. constrain `centre_line` horizontal/vertical;
7. dimension `middle` from the sketch origin using the authored position
   expressions.

The two perpendicular endpoint coordinates must have identical symbolic intent.
Equal current numbers backed by different parameters are rejected because they
could later skew the Slot.

Symbolic diagonal straight Slots remain unsupported. Fixed numeric diagonal
Slots keep the direct native path.

Arc-Slot authored points remain fixed numeric in this change; their width may
be symbolic.

## SolidCraft 0.45 semantics discovered by qualification

The common role name `length` does not mean the same authored measure for all
three straight creators:

- `slot.center_to_center`: authored end-centre distance;
- `slot.overall`: authored outer-end distance;
- `slot.center_point`: complete straight centre-line length, therefore
  **2 × authored center-to-end distance**.

SolidCraft linear position dimensions are positive distances. Forge therefore
drives middle-position dimensions with the native expression
`abs(authored_position)`; the numeric seed determines the authored side of the
origin.

`abs()` is part of SolidCraft 0.45's expression language. Forge keeps that
expression typed so component namespacing and replay dependency rewriting still
see the underlying model parameters.

These details are not inferred from the old 0.43 work. They come from the
canonical 0.45 registry, pinned upstream source and native qualification.

## Replay and pattern bindings

`sketch.draw.dimensioned` forwards the native creator reply. Forge therefore
binds `centre_line` and `middle` directly from that result.

A Slot may also be the source of a later native sketch pattern/mirror. The
profile-curves binding and the runtime `centre_line` / `middle` bindings are
merged on one command; neither may overwrite the other.

## Qualification

The existing `slot-family` baseline geometry remains unchanged so its four
independent Q3/Q6 references remain valid.

The Forge model now authors:

- one editable shared Slot width;
- editable endpoints for all three straight Slots;
- one editable shared straight-Slot Y position;
- fixed authored arc-Slot points.

The case now requires Q5. Its saved-design mutation changes, without rerunning
Forge Python:

- width 8 → 10 mm;
- straight Y -35 → -20 mm;
- each straight Slot length through one endpoint change.

The SolidCraft 0.45 run proves:

- native model verification PASS;
- visual verification PASS;
- solved five-profile native Slot sketch;
- deterministic mutated body geometry;
- successful saved-design parameter mutation/rebuild.

SolidCraft adds its own internal `d*` sketch parameters for the dimensioned
geometry. Verification therefore uses the generic
`parameter_match="subset"` contract: Forge-authored parameters are stable API
evidence; SolidCraft-generated internal dimension names are not.

## Relationship to earlier changes

- **0027** remains the history of the initial native Slot-family API, but its
  0.42 numeric-width limitation is superseded by this 0.45 qualification.
- **0030** remains relevant: fixed Slot coordinates on a parametrically sized
  attached Sketch must not accidentally inherit cancelling parent expressions.
- **0031** is historical runtime-contract work; the current canonical 0.45
  registry under `docs/reference/solidcraft/0.45.0/` is the evidence used by
  this change.
