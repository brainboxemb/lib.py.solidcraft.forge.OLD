# Native sheet contour-flange regression fixture

This non-public regression fixture qualifies Forge issue #684 against the
pinned SolidCraft 0.45 runtime.

## Intent

Create one native contour-flange sheet body from a reusable open XZ Sketch
chain:

- fixed first line feeding the native tangent arc;
- one native tangent arc with the fixed endpoint required by SolidCraft 0.45;
- one parameter-driven final line;
- one parameter-driven contour distance.

The public Forge operation is:

```python
sheet = contour.contour_flange(
    distance=contour_width,
    thickness=2.5,
    bend_radius=2.5,
    k_factor=0.44,
    rule_name="Contour Flange Rule",
)
```

The sheet rule owns thickness, K-factor and bend radius. The native
`sheet.flange(type=contour)` command receives only the rule name.

## Curve identity

The tangent arc has no authored native id. Forge therefore accumulates the
ordered curve ids with SCPF replay bindings and passes that runtime list to the
contour flange. No caller-visible or guessed SolidCraft ids are used.

## Saved-design qualification

Without rerunning Forge Python, the saved SolidCraft design changes:

- `contour_width: 50 -> 60 mm`;
- `end_height: 30 -> 35 mm`.

The rebuilt/reopened model must remain one connected closed sheet-metal body
with the same open Sketch chain.

## Flat pattern

Baseline inspection requires a recoverable flat pattern using the same sheet
rule, thickness and K-factor. SolidCraft 0.45 reports the tangent-arc contour as
continuous contour geometry rather than a discrete bend record, so this fixture
expects `bends=[]`. Bend radius is separately proven in the emitted
`sheet.manage_rules` command contract.
