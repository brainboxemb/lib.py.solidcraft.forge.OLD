# Open connected Sketch-chain regression fixture

This is the focused SolidCraft qualification fixture for Forge issue #683.

It is deliberately a **regression fixture**, not a public Verification example.
The public API/compiler contract is documented in `docs/api.md`,
`docs/requirements.md` and `docs/design.md`.

## Purpose

Prove that one standalone Sketch may contain a reusable **open** connected
line/tangent-arc chain without weakening Forge's separate closed-profile
contract.

The fixture authors:

- one parameter-driven native line;
- one native tangent arc with a fixed numeric endpoint, referencing the preceding
  line through a compiler-owned deterministic curve id;
- one final parameter-driven native line;
- parameter mutation on the surrounding line endpoints while the tangent endpoint
  remains within SolidCraft 0.45's fixed-point contract;
- one finished open Sketch chain;
- no closed Sketch profile and no solid body.

## Saved-design qualification

The initial design uses:

- `length = 40 mm`;
- `end_height = 30 mm`.

Without rerunning Forge Python, the saved SolidCraft design changes:

- `length: 40 -> 45 mm`;
- `end_height: 30 -> 35 mm`.

After mutation and save/reopen, the Sketch must still contain exactly three
connected curves, zero closed profiles and no solid body.

Machine expectations live in
[`verification/verify.py`](verification/verify.py).
