# Connected mixed-curve sheet regression fixture

This is the focused native qualification fixture for Forge issue #567.

It is deliberately a **regression fixture**, not a public Verification example.
The public API/compiler contract is documented in `docs/api.md`,
`docs/requirements.md` and `docs/design.md`.

## Purpose

Prove that one closed Sketch profile can mix native straight lines and circular
arcs and then feed `Sketch.sheet_metal()` without polygon approximation or
caller-visible SolidCraft curve ids.

The fixture uses a capsule-like blank:

- two parameter-driven straight segments;
- two parameter-driven native center-point semicircular arcs;
- one native closed Sketch profile;
- one native sheet-metal base body.

## Saved-design qualification

The initial design uses:

- `half_span = 40 mm`;
- `radius = 20 mm`;
- `thickness = 2 mm`.

Without rerunning Forge Python, the saved SolidCraft design changes:

- `half_span: 40 -> 50 mm`;
- `radius: 20 -> 25 mm`.

That mutation changes both the straight segment length and arc geometry. The
saved/reopened design must still contain one solved closed profile and one
closed sheet-metal body.

Machine expectations live in
[`verification/verify.py`](verification/verify.py).
