# Component-local Cylinder occurrence regression

This owner-layer regression fixture qualifies Forge issue #753 against the
pinned SolidCraft runtime. CAD #388 is the concrete downstream five-panel
reproducer.

## Why the old fixture was insufficient

The original retained smoke used one Box plus one native Cylinder join and two
90-degree occurrences. It remained useful as a primitive-frame check, but it did
not reproduce CAD #388. Runtime v0.3.5 therefore proved only that small shape.

The source-matched CAD acceptance of Forge v0.14.0 / SolidCraft 0.48.1 still
rendered detached cylindrical features. This fixture now preserves the relevant
history shape of the failing component before further minimization:

- tapered panel body;
- one rear-face multi-profile cut;
- 14 native Cylinder joins;
- 24 native Hole features;
- five occurrences;
- 90-degree X rotations and the alternating 180-degree [0,1,-1] rotations used
  by the product screen.

The dimensions are deliberately the same mechanical envelope used by the
downstream reproducer so presentation evidence can be compared directly.

## Expected native result

SolidCraft must contain five panel bodies at the authored screen placements.
Every joined Cylinder belongs to the reusable component definition and must
follow each copied/rotated occurrence. The generated presentation preview must
show no detached source/tool cylinders above, below or at the definition origin.

Body-envelope verification alone is not sufficient for this regression:
SolidCraft has historically reported only the intended joined body even when
stale tool geometry remained visible. The presentation preview is therefore part
of the owner investigation until the smallest failing sequence is isolated and
an automated render-level assertion is retained.

## Ownership

Do not replace native Cylinder joins with product-specific Sketch/extrude
geometry. If this owner fixture reproduces the downstream render defect, reduce
the feature sequence here and fix or block the Forge/SolidCraft layer.
