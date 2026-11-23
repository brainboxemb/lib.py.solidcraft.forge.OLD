# Native sheet edge-flange regression fixture

This non-public regression fixture qualifies Forge issue #682 against the
pinned SolidCraft 0.45 runtime.

## Intent

Start with one 80 × 40 × 2 mm native sheet base and add one native edge flange
from the right-hand sheet edge.

The public Forge operation is:

```python
sheet.flange(
    edges=[(40, 0, 2)],
    height=flange_height,
    angle=flange_angle,
)
```

The existing sheet rule owns thickness, K-factor and bend radius. The edge
flange does not repeat those material fields.

## Saved-design qualification

Without rerunning Forge Python, the saved SolidCraft design changes:

- `flange_height: 20 -> 25 mm`;
- `flange_angle: 90 -> 75 deg`.

The rebuilt/reopened model must remain one connected closed sheet-metal body.

## Flat pattern

Baseline inspection requires a recoverable flat pattern with one native bend
using the same sheet rule, thickness and bend radius.
