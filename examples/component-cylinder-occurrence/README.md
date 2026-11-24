# Component-local Cylinder occurrence regression

This non-public regression fixture qualifies Forge issue #753 against the pinned
SolidCraft runtime. CAD issue #388 is the downstream five-panel reproducer.

## Purpose

A native `Cylinder(...)` joined to a reusable component body must remain
entirely owned by that component definition. Copying and rotating occurrences
must not leave one untransformed source/tool cylinder visible at the component
definition origin.

## Model

`BossedPanel` contains:

- one centered 20 × 10 × 4 mm Box;
- one Ø4 × 4 mm native Cylinder boss;
- 0.5 mm physical overlap between boss and plate so the join is unambiguous.

Two occurrences are placed at X=-30 and X=+30 and rotated 90° around X. This
deliberately turns the component-local Z axis used by the Cylinder, matching the
ordinary HUB75 panel orientation and exercising the suspected native frame
mismatch.

## Expected native result

SolidCraft must contain two joined bodies only, with world envelopes:

- X=-40..-20, Y=-5.5..2, Z=-5..5;
- X=+20..+40, Y=-5.5..2, Z=-5..5.

The generated presentation preview must show only the two placed bossed panels.
Any extra cylinder near the definition/world origin is the regression symptom,
even if body measurements still report only the intended joined bodies.

## Ownership

The model intentionally uses Forge's public native Cylinder feature path. Do not
replace it with a product-specific sketch/extrude workaround. If the native
result is wrong, qualify the Forge/SolidCraft ownership boundary and fix or
block it there.
