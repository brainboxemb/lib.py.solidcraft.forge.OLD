# Native sheet path-flange regression fixture

This focused regression fixture qualifies Forge issue #776 against the pinned
SolidCraft 0.45 runtime.

## Intent

Start with one 80 × 40 × 2 mm native sheet base. On the right-hand top sheet
edge, create one native path flange from a line-only open Sketch chain in the
XZ plane.

The public Forge operation is:

```python
sheet.path_flange(
    edge=(40, 0, 2),
    path=path,
    radius=path_radius,
)
```

The active sheet rule continues to own thickness and K-factor. The explicit
path-flange radius overrides only this feature's bend radius.

## Saved-design qualification

Without rerunning Forge Python, the saved SolidCraft design changes:

- `path_height: 14 -> 18 mm`;
- `path_radius: 3 -> 4 mm`.

The rebuilt/reopened model must remain one connected closed sheet-metal body.

## Flat pattern

Baseline inspection requires one recoverable flat pattern with one native bend,
the path-flange radius override, and the inherited sheet rule/material values.
