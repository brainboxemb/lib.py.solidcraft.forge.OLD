# Contour flange recess replay

**Group:** `sheet-metal`
**Issue:** Forge #845

## Goal

Reproduce the smallest known downstream divergence between headless SolidCraft
replay and live GUI replay without carrying the Mounting Rail M8 product model,
assembly or repeat pattern.

## Geometry

The fixture uses the same physical section as the downstream rail:

- 250 mm length;
- 27 × 18 × 1.25 mm C-profile;
- 15 mm opening;
- R1.25 bend rule, K=0.40;
- one Ø12.5 mm through-cut centred across the broad 27 mm back face;
- cut centre Y=37.5 mm.

The cut is geometrically clear of both profile bends. The downstream standalone
rail fails live at this exact first-cut position. The 1000 mm assembly variant
also fails with the first cut at Y=12.5 mm.

## Replay contract

Forge emits the contour flange, binds the broad +Z face with `model.faces`,
attaches the circular Sketch to that exact face and then emits the through-all
cut.

Headless replay currently persists an intermediate `.sc` file between replay
phases. Live replay uses the same replay document but keeps the design in the
same GUI session across the binding boundary. #845 exists to determine whether
that state difference is material.

Do not move the cut as a workaround; the physical geometry is the regression.
