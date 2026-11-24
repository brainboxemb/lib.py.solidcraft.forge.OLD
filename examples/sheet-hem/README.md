# Native sheet hem regression fixture

This non-public regression fixture qualifies Forge issue #773 against the
pinned SolidCraft 0.45 runtime.

## Intent

Start with one 80 × 40 × 2 mm native sheet base and add one native hem on the
right-hand sheet edge.

The public Forge operation is:

```python
sheet.hem(
    edges=[(40, 0, 2)],
    length=hem_length,
    gap=hem_gap,
)
```

The existing sheet rule owns thickness, K-factor and bend radius. The hem does
not restate those material fields.

## Saved-design qualification

Without rerunning Forge Python, the saved SolidCraft design changes:

- `hem_length: 12 -> 16 mm`;
- `hem_gap: 4 -> 5 mm`.

The rebuilt/reopened model must remain one connected closed sheet-metal body.

## Flat pattern

Baseline inspection requires a recoverable flat pattern with native bend
history using the same sheet rule, thickness and K-factor.
